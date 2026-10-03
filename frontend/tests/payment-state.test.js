import assert from 'node:assert/strict'
import { test } from 'node:test'
import { beginPayment, readPayment, updatePayment, clearConfirmedPayment, classifyPaymentStatus } from '../src/utils/payment-state.js'

function storage() {
  const values = new Map()
  return { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value), removeItem: key => values.delete(key) }
}

test('a pending attempt survives reload and cannot be silently replaced', () => {
  const store = storage()
  const first = beginPayment(store, { amount: '12.50', category: 'Ofertas' })
  assert.match(first.key, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/)
  assert.equal(readPayment(store).key, first.key)
  assert.throws(() => beginPayment(store, { amount: '20.00' }))
  assert.throws(() => clearConfirmedPayment(store))
  updatePayment(store, { state: 'unknown' })
  assert.equal(readPayment(store).key, first.key)
  assert.throws(() => clearConfirmedPayment(store))
})

test('only confirmed success permits explicitly starting another contribution', () => {
  const store = storage()
  const first = beginPayment(store, { amount: '12.50', phone: 'private', email: 'private' })
  assert.equal(readPayment(store).phone, undefined)
  assert.equal(readPayment(store).email, undefined)
  updatePayment(store, { state: 'success', requestId: 'provider-reference' })
  assert.equal(readPayment(store).requestId, 'provider-reference')
  clearConfirmedPayment(store)
  assert.notEqual(beginPayment(store, { amount: '12.50' }).key, first.key)
})

test('ambiguous gateway messages and local timeouts never imply success or no debit', () => {
  assert.equal(classifyPaymentStatus({ Status: '000', Message: 'Success' }), 'success')
  assert.equal(classifyPaymentStatus({ Status: '000', Message: 'Pending' }), 'waiting')
  for (const result of [null, {}, { Status: '000', Message: 'anything' }, { Status: '101', Message: 'expired' }, { Status: '020', Message: 'cancelled' }]) {
    assert.equal(classifyPaymentStatus(result), 'unknown')
  }
})

test('the real form respects a not-sent retry delay and preserves uncertain attempts across reload', async () => {
  const { JSDOM } = await import('jsdom')
  const { readFile } = await import('node:fs/promises')
  const { parse, compileScript } = await import('@vue/compiler-sfc')
  const dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'https://example.test' })
  for (const name of ['window', 'document', 'Node', 'Element', 'HTMLElement', 'SVGElement', 'sessionStorage']) {
    Object.defineProperty(globalThis, name, { value: dom.window[name], configurable: true })
  }
  const submitted = []
  const recovered = []
  const originalNow = Date.now
  globalThis.__paymentTestApi = {
    getDonationsContent: async () => ({ value: {} }),
    submitDonationMbway: async (...args) => {
      submitted.push(args)
      if (submitted.length === 1) throw { response: { status: 429, attemptState: 'not-sent', retryAfter: '300' } }
      throw new Error('network timeout')
    },
    recoverDonationAttempt: async (key) => { recovered.push(key); throw new Error('outcome unknown') },
    getPaymentStatus: async () => ({ Status: '000', Message: 'Pending' }),
  }
  const apiModule = 'data:text/javascript;base64,' + Buffer.from(
    'export const { getDonationsContent, submitDonationMbway, recoverDonationAttempt, getPaymentStatus } = globalThis.__paymentTestApi',
  ).toString('base64')
  const componentUrl = new URL('../src/views/DonationFormView.vue', import.meta.url)
  const { descriptor } = parse(await readFile(componentUrl, 'utf8'))
  const { content } = compileScript(descriptor, { id: 'payment-recovery-test', inlineTemplate: true })
  const source = content
    .replace(/^import logoWhite .+$/m, "const logoWhite = ''")
    .replace(/^import MbwayLogo .+$/m, 'const MbwayLogo = { render: () => null }')
    .replace(/from (['"])([^'"]+)\1/g, (_, quote, specifier) => {
      const url = specifier === '../services/api' ? apiModule : specifier.startsWith('.')
        ? new URL(`${specifier}.js`, componentUrl).href : import.meta.resolve(specifier)
      return `from ${JSON.stringify(url)}`
    })
  const { default: Form } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)
  const { createApp, h, nextTick } = await import('vue')
  const host = document.createElement('div')
  document.body.append(host)
  const mount = () => {
    const app = createApp(Form)
    app.component('router-link', { render() { return h('a', this.$slots.default?.()) } })
    app.mount(host)
    return app
  }
  const flush = async () => { await new Promise(resolve => setTimeout(resolve, 0)); await nextTick() }
  let app = mount()
  try {
    await flush()
    for (const [selector, value] of [['input[type=number]', '12.50'], ['input[type=tel]', '912345678']]) {
      const input = host.querySelector(selector)
      input.value = value
      input.dispatchEvent(new window.Event('input', { bubbles: true }))
    }
    const terms = host.querySelector('input[type=checkbox]')
    terms.checked = true
    terms.dispatchEvent(new window.Event('change', { bubbles: true }))
    await nextTick()
    const form = host.querySelector('form')
    form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }))
    form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }))
    await flush()
    assert.equal(submitted.length, 1)
    assert.equal(readPayment(sessionStorage).state, 'not_sent')
    assert.ok(host.querySelector('form'))
    host.querySelector('form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }))
    await flush()
    assert.equal(submitted.length, 1)
    Date.now = () => originalNow() + 300001
    const correctedPhone = host.querySelector('input[type=tel]')
    correctedPhone.value = '912345678'
    correctedPhone.dispatchEvent(new window.Event('input', { bubbles: true }))
    await nextTick()
    host.querySelector('form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }))
    await flush()
    assert.equal(submitted.length, 2)
    assert.equal(submitted[0][4], submitted[1][4])
    assert.match(host.textContent, /Estado do pagamento por confirmar/)
    assert.equal(host.querySelector('form'), null)
    const key = submitted[0][4]
    assert.equal(readPayment(sessionStorage).key, key)
    app.unmount()
    app = mount()
    await flush()
    assert.deepEqual(recovered, [key])
    assert.equal(submitted.length, 2)
    assert.equal(readPayment(sessionStorage).key, key)
    assert.match(host.textContent, /Estado do pagamento por confirmar/)
  } finally {
    app.unmount()
    host.remove()
    dom.window.close()
    delete globalThis.__paymentTestApi
    Date.now = originalNow
  }
})
