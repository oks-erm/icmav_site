// #region CONSTANTS & AUTH TOKEN HELPERS

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
const TOKEN_STORAGE_KEY = 'icmav_admin_token'

export function getAuthToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_STORAGE_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
  }
}

export function clearAuthToken() {
  localStorage.removeItem(TOKEN_STORAGE_KEY)
}

export function hasAuthToken() {
  return !!getAuthToken()
}

function getAuthHeaders(additionalHeaders = {}) {
  const token = getAuthToken()
  const headers = { ...additionalHeaders }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

async function handleResponseError(response, defaultMsg) {
  if (response.status === 401) {
    clearAuthToken()
    throw new Error('Sessão expirada ou não autorizada. Por favor inicia sessão novamente.')
  }
  const errorData = await response.json().catch(() => null)
  const detail = errorData?.detail
  if (typeof detail === 'string') {
    throw new Error(detail)
  } else if (Array.isArray(detail)) {
    const msg = detail.map(e => (typeof e === 'object' ? (e.msg || JSON.stringify(e)) : String(e))).join(', ')
    throw new Error(msg || defaultMsg)
  } else if (detail && typeof detail === 'object') {
    throw new Error(JSON.stringify(detail))
  }
  throw new Error(defaultMsg)
}

// #endregion

// #region IN-MEMORY CACHING & IN-FLIGHT DEDUPLICATION

const memoryCache = new Map()
const inFlightRequests = new Map()

/**
 * Faz fetch com deduplicação de pedidos concorrentes e cache de curta duração.
 */
async function cachedGet(url, ttlMs = 15000) {
  const now = Date.now()
  const cached = memoryCache.get(url)

  if (cached && now - cached.timestamp < ttlMs) {
    return cached.data
  }

  // Se já houver um pedido em voo para este mesmo URL, partilhar a mesma Promise
  if (inFlightRequests.has(url)) {
    return inFlightRequests.get(url)
  }

  const requestPromise = fetch(url)
    .then(async (response) => {
      if (!response.ok) {
        await handleResponseError(response, 'Erro ao carregar dados')
      }
      const data = await response.json()
      memoryCache.set(url, { data, timestamp: Date.now() })
      return data
    })
    .finally(() => {
      inFlightRequests.delete(url)
    })

  inFlightRequests.set(url, requestPromise)
  return requestPromise
}

export function invalidateCache(urlPattern = '') {
  if (!urlPattern) {
    memoryCache.clear()
    return
  }
  for (const key of memoryCache.keys()) {
    if (key.includes(urlPattern)) {
      memoryCache.delete(key)
    }
  }
}

// #endregion

// #region ADMIN LOGIN

export async function adminLogin(username, password) {
  const response = await fetch(`${API_BASE_URL}/admin/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw new Error(errorData?.detail || 'Credenciais inválidas')
  }

  const data = await response.json()
  if (data.access_token) {
    setAuthToken(data.access_token)
  }
  return data
}

// #endregion

// #region WELCOME SECTION

export async function getWelcomeContent() {
  return cachedGet(`${API_BASE_URL}/settings/welcome`)
}

export async function updateWelcomeContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/welcome`, {
    method: 'PUT',
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ value }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar conteúdo')
  }
  invalidateCache('/settings/welcome')
  return response.json()
}

export async function resetWelcomeContent() {
  const response = await fetch(`${API_BASE_URL}/settings/welcome/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor conteúdo Welcome')
  }
  invalidateCache('/settings/welcome')
  return response.json()
}

// #endregion

// #region PURPOSES SECTION

export async function getPurposesContent() {
  return cachedGet(`${API_BASE_URL}/settings/purposes`)
}

export async function updatePurposesContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/purposes`, {
    method: 'PUT',
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar propósitos')
  }
  invalidateCache('/settings/purposes')
  return response.json()
}

export async function resetPurposesContent() {
  const response = await fetch(`${API_BASE_URL}/settings/purposes/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor propósitos')
  }
  invalidateCache('/settings/purposes')
  return response.json()
}

// #endregion

// #region PASTORAL TEAM SECTION

export async function getPastoralTeamContent() {
  return cachedGet(`${API_BASE_URL}/settings/pastoral-team`)
}

export async function updatePastoralTeamContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/pastoral-team`, {
    method: 'PUT',
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar equipa pastoral')
  }
  invalidateCache('/settings/pastoral-team')
  return response.json()
}

export async function resetPastoralTeamContent() {
  const response = await fetch(`${API_BASE_URL}/settings/pastoral-team/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor equipa pastoral')
  }
  invalidateCache('/settings/pastoral-team')
  return response.json()
}

export async function uploadPastoralTeamPhoto(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/settings/pastoral-team/upload-photo`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao fazer upload da foto')
  }
  invalidateCache('/settings/pastoral-team')
  return response.json()
}

export async function getMessageContent() {
  return cachedGet(`${API_BASE_URL}/settings/message`)
}

export async function updateMessageContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/message`, {
    method: 'PUT',
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ value }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar conteúdo Message')
  }
  invalidateCache('/settings/message')
  return response.json()
}

export async function resetMessageContent() {
  const response = await fetch(`${API_BASE_URL}/settings/message/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor conteúdo Message')
  }
  invalidateCache('/settings/message')
  return response.json()
}

// #endregion

// #region MINISTRIES PRESENTATION SECTION

export async function getMinistriesPresentationContent() {
  return cachedGet(`${API_BASE_URL}/settings/ministries-presentation`)
}

export async function updateMinistriesPresentationContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/ministries-presentation`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar conteúdo Ministérios')
  }
  invalidateCache('/settings/ministries-presentation')
  return response.json()
}

export async function resetMinistriesPresentationContent() {
  const response = await fetch(`${API_BASE_URL}/settings/ministries-presentation/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor conteúdo Ministérios')
  }
  invalidateCache('/settings/ministries-presentation')
  return response.json()
}

export async function uploadMinistryLeaderPhoto(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/settings/ministries-presentation/upload-photo`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao carregar foto do líder')
  }
  invalidateCache('/settings/ministries-presentation')
  return response.json()
}

export async function uploadMinistryMedia(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/settings/ministries-presentation/upload-media`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao carregar conteúdo multimédia')
  }
  invalidateCache('/settings/ministries-presentation')
  return response.json()
}

// #endregion

// #region SERVICES BANNER SECTION

export async function getServicesBannerContent() {
  return cachedGet(`${API_BASE_URL}/settings/services-banner`)
}

export async function updateServicesBannerContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/services-banner`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Services Banner')
  }
  invalidateCache('/settings/services-banner')
  return response.json()
}

export async function resetServicesBannerContent() {
  const response = await fetch(`${API_BASE_URL}/settings/services-banner/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Services Banner')
  }
  invalidateCache('/settings/services-banner')
  return response.json()
}

// #endregion

// #region LOCAL GATHERINGS SECTION

export async function getLocalGatheringsContent() {
  return cachedGet(`${API_BASE_URL}/settings/local-gatherings`)
}

export async function updateLocalGatheringsContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/local-gatherings`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Encontros Locais')
  }
  invalidateCache('/settings/local-gatherings')
  return response.json()
}

export async function resetLocalGatheringsContent() {
  const response = await fetch(`${API_BASE_URL}/settings/local-gatherings/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Encontros Locais')
  }
  invalidateCache('/settings/local-gatherings')
  return response.json()
}

export async function getLocalGatheringOptions() {
  return cachedGet(`${API_BASE_URL}/settings/local-gathering-options`)
}

export async function updateLocalGatheringOptions(value) {
  const response = await fetch(`${API_BASE_URL}/settings/local-gathering-options`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar opções de Pequenos Grupos')
  }
  invalidateCache('/settings/local-gathering-options')
  return response.json()
}

export async function resetLocalGatheringOptions() {
  const response = await fetch(`${API_BASE_URL}/settings/local-gathering-options/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor opções de Pequenos Grupos')
  }
  invalidateCache('/settings/local-gathering-options')
  return response.json()
}

// #endregion

// #region GALLERY SECTION

export async function getGalleryContent() {
  return cachedGet(`${API_BASE_URL}/settings/gallery`)
}

export async function updateGalleryContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/gallery`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Galeria')
  }
  invalidateCache('/settings/gallery')
  return response.json()
}

export async function resetGalleryContent() {
  const response = await fetch(`${API_BASE_URL}/settings/gallery/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Galeria')
  }
  invalidateCache('/settings/gallery')
  return response.json()
}

export async function uploadGalleryPhoto(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/settings/gallery/upload-photo`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao fazer upload da foto da galeria')
  }
  invalidateCache('/settings/gallery')
  return response.json()
}

// #endregion

// #region HELP REQUEST SECTION

export async function getHelpRequestContent() {
  return cachedGet(`${API_BASE_URL}/settings/help-request`)
}

export async function updateHelpRequestContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/help-request`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Pedido de Ajuda')
  }
  invalidateCache('/settings/help-request')
  return response.json()
}

export async function resetHelpRequestContent() {
  const response = await fetch(`${API_BASE_URL}/settings/help-request/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Pedido de Ajuda')
  }
  invalidateCache('/settings/help-request')
  return response.json()
}

// #endregion

// #region SOCIAL MEDIA SECTION

export async function getSocialMediaContent() {
  return cachedGet(`${API_BASE_URL}/settings/social-media`)
}

export async function updateSocialMediaContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/social-media`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Redes Sociais')
  }
  invalidateCache('/settings/social-media')
  return response.json()
}

export async function resetSocialMediaContent() {
  const response = await fetch(`${API_BASE_URL}/settings/social-media/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Redes Sociais')
  }
  invalidateCache('/settings/social-media')
  return response.json()
}

// #endregion

// #region DONATIONS SECTION

export async function getDonationsContent() {
  return cachedGet(`${API_BASE_URL}/settings/donations`)
}

export async function updateDonationsContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/donations`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: typeof value === 'string' ? value : JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Contribuições')
  }
  invalidateCache('/settings/donations')
  return response.json()
}

export async function resetDonationsContent() {
  const response = await fetch(`${API_BASE_URL}/settings/donations/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Contribuições')
  }
  invalidateCache('/settings/donations')
  return response.json()
}

// #endregion

// #region LOCATIONS SECTION

export async function getLocationsContent() {
  return cachedGet(`${API_BASE_URL}/settings/locations`)
}

export async function updateLocationsContent(value) {
  const response = await fetch(`${API_BASE_URL}/settings/locations`, {
    method: 'PUT',
    headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ value: JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar Localizações')
  }
  invalidateCache('/settings/locations')
  return response.json()
}

export async function resetLocationsContent() {
  const response = await fetch(`${API_BASE_URL}/settings/locations/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor Localizações')
  }
  invalidateCache('/settings/locations')
  return response.json()
}

// #endregion

// #region IFTHENPAY / MB WAY GATEWAY CONFIG

export async function getIfthenpayConfig() {
  const response = await fetch(`${API_BASE_URL}/settings/ifthenpay-config`, {
    headers: getAuthHeaders(),
  })
  if (!response.ok) {
    await handleResponseError(response, 'Erro ao carregar configuração IFTHENPAY')
  }
  return response.json()
}

export async function updateIfthenpayConfig(value) {
  const response = await fetch(`${API_BASE_URL}/settings/ifthenpay-config`, {
    method: 'PUT',
    headers: getAuthHeaders({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ value: JSON.stringify(value) }),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao guardar configuração IFTHENPAY')
  }
  return response.json()
}

export async function resetIfthenpayConfig() {
  const response = await fetch(`${API_BASE_URL}/settings/ifthenpay-config/reset`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    await handleResponseError(response, 'Erro ao repor configuração IFTHENPAY')
  }
  return response.json()
}

// Aliases para retrocompatibilidade
export const getSibsConfig = getIfthenpayConfig
export const updateSibsConfig = updateIfthenpayConfig
export const resetSibsConfig = resetIfthenpayConfig

// #endregion

// #region DONATION FORM (PUBLIC)

export async function testBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error('Não foi possível comunicar com o backend.')
  }
  return response.json()
}

export async function submitDonationMbway(amount, phone, category, email = null) {
  const response = await fetch(`${API_BASE_URL}/donate/mbway`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount, phone, category, email }),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw { response: { data: errorData } }
  }
  return response.json()
}

export async function getPaymentStatus(requestId) {
  const response = await fetch(`${API_BASE_URL}/payment-status/${requestId}`)
  if (!response.ok) {
    const errorData = await response.json().catch(() => null)
    throw { response: { data: errorData } }
  }
  return response.json()
}

// #endregion