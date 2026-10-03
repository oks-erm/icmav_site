// Keep only recovery metadata in this tab; never persist phone, email or fiscal data.
const STORAGE_KEY = 'icmav_pending_payment'
const KEY_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/

export function readPayment(storage) {
  const raw = storage.getItem(STORAGE_KEY)
  if (!raw) return null
  const value = JSON.parse(raw)
  if (!value || !KEY_PATTERN.test(value.key) || !Number.isFinite(value.startedAt)) {
    throw new Error('Não foi possível recuperar o pedido. Contacta a tesouraria antes de repetir o pagamento.')
  }
  return value
}

export function beginPayment(storage, { amount, category }) {
  if (readPayment(storage)) throw new Error('Existe um pedido de pagamento por confirmar.')
  const attempt = { key: crypto.randomUUID(), amount, category, startedAt: Date.now(), state: 'unknown', requestId: null }
  storage.setItem(STORAGE_KEY, JSON.stringify(attempt))
  return attempt
}

export function updatePayment(storage, { state, requestId, amount, category, retryAt }) {
  const attempt = readPayment(storage)
  if (!attempt) throw new Error('Pedido de pagamento não encontrado.')
  if (state) attempt.state = state
  if (requestId) attempt.requestId = requestId
  if (amount !== undefined) attempt.amount = amount
  if (category !== undefined) attempt.category = category
  if (retryAt !== undefined) attempt.retryAt = retryAt
  storage.setItem(STORAGE_KEY, JSON.stringify(attempt))
  return attempt
}

export function clearConfirmedPayment(storage) {
  const attempt = readPayment(storage)
  if (attempt && attempt.state !== 'success') throw new Error('Confirma o estado do pagamento antes de iniciar outro.')
  storage.removeItem(STORAGE_KEY)
}

export function classifyPaymentStatus(result) {
  if (result?.Status === '000' && result.Message === 'Success') return 'success'
  if (result?.Status === '000' && result.Message === 'Pending') return 'waiting'
  return 'unknown'
}
