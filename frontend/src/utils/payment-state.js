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

const TERMINAL_CLEARABLE_STATES = new Set(['success', 'rejected', 'expired', 'declined'])

function generateUUID() {
  if (typeof crypto?.randomUUID === 'function') {
    return crypto.randomUUID()
  }
  const bytes = crypto.getRandomValues(new Uint8Array(16))
  bytes[6] = (bytes[6] & 0x0f) | 0x40
  bytes[8] = (bytes[8] & 0x3f) | 0x80
  const hex = [...bytes].map(b => b.toString(16).padStart(2, '0')).join('')
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
}

export function beginPayment(storage, { amount, category }) {
  if (readPayment(storage)) throw new Error('Existe um pedido de pagamento por confirmar.')
  const attempt = { key: generateUUID(), amount, category, startedAt: Date.now(), state: 'unknown', requestId: null }
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
  if (attempt && !TERMINAL_CLEARABLE_STATES.has(attempt.state)) {
    throw new Error('Confirma o estado do pagamento antes de iniciar outro.')
  }
  storage.removeItem(STORAGE_KEY)
}

export function dismissUnknownAttempt(storage) {
  storage.removeItem(STORAGE_KEY)
}

export function classifyPaymentStatus(result) {
  if (!result || typeof result !== 'object') return 'unknown'
  const status = String(result.Status || '').trim()
  const msg = String(result.Message || '').trim()
  const msgLower = msg.toLowerCase()

  if (status === '000') {
    if (msg === 'Success' || msgLower === 'success' || msgLower === 'sucesso') return 'success'
    if (msg === 'Pending' || msgLower === 'pending' || msgLower === 'pendente') return 'waiting'
    return 'unknown'
  }
  if (status === '020') return 'rejected'
  if (status === '101') return 'expired'
  if (status === '122' || status === '100') return 'declined'
  return 'unknown'
}
