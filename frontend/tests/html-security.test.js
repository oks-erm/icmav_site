import assert from 'node:assert/strict'
import { after, test } from 'node:test'
import { readFile } from 'node:fs/promises'
import { compileScript, parse } from '@vue/compiler-sfc'
import { JSDOM } from 'jsdom'

const dom = new JSDOM('<!doctype html><html><body></body></html>')
const browserGlobals = ['window', 'document', 'navigator', 'Node', 'Element', 'HTMLElement', 'SVGElement', 'Text', 'MutationObserver', 'DOMParser', 'getComputedStyle']
const originalGlobals = new Map(browserGlobals.map(name => [name, Object.getOwnPropertyDescriptor(globalThis, name)]))
for (const name of browserGlobals) {
  Object.defineProperty(globalThis, name, { configurable: true, value: dom.window[name] })
}
const { sanitizeHtml } = await import('../src/utils/sanitize-html.js')

after(() => {
  for (const [name, descriptor] of originalGlobals) {
    if (descriptor) Object.defineProperty(globalThis, name, descriptor)
    else delete globalThis[name]
  }
  dom.window.close()
})

function fragment(html) {
  const template = dom.window.document.createElement('template')
  template.innerHTML = sanitizeHtml(html)
  return template.content
}

test('rich text removes event handlers and executable or embedded elements', () => {
  const result = fragment(`
    <p onclick="alert(1)">Welcome <strong onmouseover="alert(2)">friend</strong></p>
    <img src="x" onerror="alert(3)">
    <script>alert(4)</script>
    <svg onload="alert(5)"><a xlink:href="javascript:alert(6)">SVG</a></svg>
    <math><mtext><img src="x" onerror="alert(7)"></mtext></math>
    <iframe srcdoc="<script>alert(8)</script>"></iframe>
    <object data="https://example.com"></object>
    <form><input autofocus onfocus="alert(9)"></form>
    <style>body { display: none }</style>
  `)
  assert.equal(result.querySelector('script, svg, math, img, iframe, object, form, input, style'), null)
  for (const element of result.querySelectorAll('*')) {
    assert.ok([...element.attributes].every(attribute => !attribute.name.startsWith('on')))
  }
  assert.equal(result.querySelector('p').textContent, 'Welcome friend')
  assert.equal(result.querySelector('strong').textContent, 'friend')
})

test('rich text rejects obfuscated executable link protocols', () => {
  for (const href of ['javascript:alert(1)', 'jav&#x61;script:alert(1)', 'java&#10;script:alert(1)', 'vbscript:msgbox(1)', 'data:text/html,<script>alert(1)</script>']) {
    const result = fragment(`<a href="${href}">Read more</a>`)
    assert.equal(result.querySelector('a').getAttribute('href'), null, href)
    assert.equal(result.textContent, 'Read more')
  }
})

test('rich text preserves the supported Quill formatting and safe links', () => {
  const result = fragment(`
    <h1>Title</h1><h2>Subtitle</h2><h3>Section</h3>
    <p class="ql-align-center"><strong>Bold</strong><em>Italic</em><u>Underline</u><s>Strike</s><br></p>
    <ol><li data-list="bullet" class="ql-indent-1"><span class="ql-ui" contenteditable="false"></span>Item</li></ol>
    <a href="https://example.com/path" target="_blank">Website</a>
    <a href="mailto:hello@example.com">Email</a><a href="/contact">Contact</a>
  `)
  assert.equal(result.querySelectorAll('h1, h2, h3, strong, em, u, s, br').length, 8)
  assert.equal(result.querySelector('p').className, 'ql-align-center')
  assert.equal(result.querySelector('li').getAttribute('data-list'), 'bullet')
  assert.equal(result.querySelector('li').className, 'ql-indent-1')
  assert.equal(result.querySelector('span').className, 'ql-ui')
  const links = result.querySelectorAll('a')
  assert.equal(links[0].href, 'https://example.com/path')
  assert.equal(links[0].target, '_blank')
  assert.ok(links[0].relList.contains('noopener'))
  assert.ok(links[0].relList.contains('noreferrer'))
  assert.equal(links[1].getAttribute('href'), 'mailto:hello@example.com')
  assert.equal(links[2].getAttribute('href'), '/contact')
})

test('rich text strips CSS injection and DOM clobbering attributes', () => {
  const result = fragment('<p id="location" name="cookie" style="position:fixed;inset:0" data-extra="unsafe">Text</p>')
  assert.equal(result.querySelector('p').attributes.length, 0)
  assert.equal(result.textContent, 'Text')
})

test('rich text treats absent or malformed content as empty', () => {
  for (const value of [null, undefined, false, 0, {}, []]) {
    assert.equal(sanitizeHtml(value), '')
  }
  assert.equal(sanitizeHtml(''), '')
})

test('the real editor sanitizes both initial and updated stored HTML before DOM insertion', async () => {
  const componentUrl = new URL('../src/components/RichTextEditor.vue', import.meta.url)
  const { descriptor } = parse(await readFile(componentUrl, 'utf8'))
  // Compile the actual SFC for Node, ignoring stylesheet imports only.
  const { content } = compileScript(descriptor, { id: 'editor-security', inlineTemplate: true })
  const moduleSource = content
    .replace(/^import ['"][^'"]+\.css['"]\s*$/gm, '')
    .replace(/from (['"])([^'"]+)\1/g, (_, quote, specifier) => {
      const url = specifier.startsWith('.')
        ? new URL(`${specifier}.js`, componentUrl).href
        : import.meta.resolve(specifier)
      return `from ${JSON.stringify(url)}`
    })
  const { default: Editor } = await import(`data:text/javascript;base64,${Buffer.from(moduleSource).toString('base64')}`)
  const { createApp, h, nextTick, ref } = await import('vue')
  const value = ref('<p onclick="alert(1)"><strong>Initial</strong><img src="x" onerror="alert(2)"></p>')
  const host = dom.window.document.createElement('div')
  dom.window.document.body.append(host)
  const app = createApp({ render: () => h(Editor, { modelValue: value.value }) })
  try {
    app.mount(host)
    const editor = host.querySelector('.ql-editor')
    assert.equal(editor.querySelector('img, [onclick], [onerror]'), null)
    assert.equal(editor.querySelector('strong').textContent, 'Initial')

    // Let Quill finish observing the initial content before updating the prop.
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 0))
    value.value = '<h2>Updated</h2><svg onload="alert(3)"></svg><p><a href="javascript:alert(4)">Link</a></p>'
    await nextTick()
    assert.equal(editor.querySelector('svg, [onload], [href^="javascript:"]'), null)
    assert.equal(editor.querySelector('h2').textContent, 'Updated')
    assert.ok(editor.textContent.includes('Link'))

    // Quill's unpatched HTML-export advisory involves video/formula embeds.
    // The application accepts only its text toolbar formats and sanitizes HTML.
    const { default: Quill } = await import('quill')
    const instance = Quill.find(host.querySelector('.ql-container'))
    assert.throws(() => instance.insertEmbed(0, 'video', 'https://example.invalid/video', 'user'), /Unable to create video blot/)
    assert.throws(() => instance.insertEmbed(0, 'formula', 'untrusted formula', 'user'), /Unable to create formula blot/)
    await nextTick()
    assert.equal(editor.querySelector('iframe, video'), null)
    assert.equal(instance.getContents().ops.some(op => typeof op.insert === 'object' && 'video' in op.insert), false)
  } finally {
    app.unmount()
    host.remove()
  }
})
