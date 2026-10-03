<!-- src/views/AdminView.vue -->
<template>
  <div class="min-h-screen flex flex-col bg-[#f3f4f6]">
    <StickyHeader />

    <section class="admin-page flex-1">
      <!-- ═══════════════════════════════ LOGIN ═══════════════════════════════ -->
      <div class="admin-card login-card" v-if="!isAuthenticated">
        <h1>Administração</h1>
        <input v-model="username" type="text" placeholder="Utilizador" @keyup.enter="handleLogin" />
        <input v-model="password" type="password" placeholder="Palavra-passe" @keyup.enter="handleLogin" />
        <button @click="handleLogin" :disabled="isLoggingIn">
          {{ isLoggingIn ? 'A entrar…' : 'Entrar' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

    <!-- ═══════════════════════════════ ADMIN PANEL ═══════════════════════════════ -->
    <div class="admin-card" v-else>
      <div class="panel-header">
        <div class="header-title-group">
          <h1>Gestão do conteúdo</h1>
          <span v-if="hasUnsavedChanges" class="unsaved-badge">
            <i class="fa-solid fa-circle-dot"></i> Alterações por guardar
          </span>
        </div>
        <button type="button" class="secondary-btn" @click="handleLogout">Terminar sessão</button>
      </div>

      <!-- Feedback notifications with close button -->
      <div v-if="success" class="alert-box alert-success">
        <span>{{ success }}</span>
        <button type="button" class="alert-close" @click="success = ''">&times;</button>
      </div>
      <div v-if="error" class="alert-box alert-error">
        <span>{{ error }}</span>
        <button type="button" class="alert-close" @click="error = ''">&times;</button>
      </div>

      <!-- ── Loading overlay ──────────────────────────────────────────── -->
      <div v-if="isLoadingData" class="loading-state">
        <span>A carregar dados…</span>
      </div>

      <template v-else>
        <div class="global-actions">
          <button type="button" class="secondary-btn" @click="openAllSections">Abrir Todos</button>
          <button type="button" class="secondary-btn" @click="closeAllSections">Fechar Todos</button>
        </div>

        <div class="sections-list">
          <!-- 1. WELCOME -->
          <AdminSectionWelcome
            v-model="infoContent"
            :is-open="openSections.welcome"
            @toggle="toggleSection('welcome')"
            @reset="handleResetWelcome"
          />

          <!-- 2. MESSAGE -->
          <AdminSectionMessage
            v-model="messageContent"
            :is-open="openSections.message"
            @toggle="toggleSection('message')"
            @reset="handleResetMessage"
          />

          <!-- 3. PURPOSES -->
          <AdminSectionPurposes
            v-model="purposes"
            :is-open="openSections.purposes"
            @toggle="toggleSection('purposes')"
            @reset="handleResetPurposes"
          />

          <!-- 4. PASTORAL TEAM -->
          <AdminSectionPastoralTeam
            v-model="pastoralTeam"
            :is-open="openSections.pastoralTeam"
            @toggle="toggleSection('pastoralTeam')"
            @reset="handleResetPastoralTeam"
            @notify="handleNotification"
          />

          <!-- 5. MINISTRIES -->
          <AdminSectionMinistries
            v-model="ministries"
            :is-open="openSections.ministries"
            @toggle="toggleSection('ministries')"
            @reset="handleResetMinistriesPresentation"
            @notify="handleNotification"
          />

          <!-- 6. SERVICES BANNER -->
          <AdminSectionServicesBanner
            v-model="servicesBannerContent"
            :is-open="openSections.servicesBanner"
            @toggle="toggleSection('servicesBanner')"
            @reset="handleResetServicesBanner"
          />

          <!-- 7. LOCAL GATHERINGS -->
          <AdminSectionLocalGatherings
            v-model="localGatheringsData"
            :is-open="openSections.localGatherings"
            @toggle="toggleSection('localGatherings')"
            @reset="handleResetLocalGatherings"
          />

          <!-- 8. LOCAL GATHERING OPTIONS -->
          <AdminSectionLocalGatheringOptions
            v-model="localGatheringOptions"
            :is-open="openSections.localGatheringOptions"
            @toggle="toggleSection('localGatheringOptions')"
            @reset="handleResetLocalGatheringOptions"
          />

          <!-- 9. GALLERY -->
          <AdminSectionGallery
            v-model="galleryImages"
            :is-open="openSections.gallery"
            @toggle="toggleSection('gallery')"
            @reset="handleResetGallery"
            @notify="handleNotification"
          />

          <!-- 10. SOCIAL MEDIA -->
          <AdminSectionSocialMedia
            v-model="socialMedia"
            :is-open="openSections.socialMedia"
            @toggle="toggleSection('socialMedia')"
            @reset="handleResetSocialMedia"
          />

          <!-- 11. DONATIONS (Apresentação, Categorias, Transferência Bancária e Gateway IFTHENPAY) -->
          <AdminSectionDonations
            v-model="donationsData"
            v-model:sibs="sibsConfig"
            :is-open="openSections.donations"
            @toggle="toggleSection('donations')"
            @reset="handleResetDonations"
          />

          <!-- 12. LOCATIONS -->
          <AdminSectionLocations
            v-model="locations"
            v-model:google-maps="googleMapsConfig"
            :is-open="openSections.locations"
            @toggle="toggleSection('locations')"
            @reset="handleResetLocations"
          />
        </div>

        <!-- SAVE ROW -->
        <div class="save-row">
          <button class="save-btn" @click="handleSave" :disabled="isSaving">
            {{ isSaving ? 'A guardar…' : 'Guardar tudo' }}
          </button>
        </div>
      </template>
    </div>
  </section>

  <Footer />
</div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import StickyHeader from '../components/StickyHeader.vue'
import Footer from '../components/Footer.vue'

import AdminSectionWelcome from '../components/admin/AdminSectionWelcome.vue'
import AdminSectionMessage from '../components/admin/AdminSectionMessage.vue'
import AdminSectionPurposes from '../components/admin/AdminSectionPurposes.vue'
import AdminSectionPastoralTeam from '../components/admin/AdminSectionPastoralTeam.vue'
import AdminSectionMinistries from '../components/admin/AdminSectionMinistries.vue'
import AdminSectionServicesBanner from '../components/admin/AdminSectionServicesBanner.vue'
import AdminSectionLocalGatherings from '../components/admin/AdminSectionLocalGatherings.vue'
import AdminSectionLocalGatheringOptions from '../components/admin/AdminSectionLocalGatheringOptions.vue'
import AdminSectionGallery from '../components/admin/AdminSectionGallery.vue'
import AdminSectionSocialMedia from '../components/admin/AdminSectionSocialMedia.vue'
import AdminSectionDonations from '../components/admin/AdminSectionDonations.vue'
import AdminSectionLocations from '../components/admin/AdminSectionLocations.vue'

import {
  adminLogin,
  hasAuthToken as checkIsAuthenticated,
  clearAuthToken,
  getWelcomeContent,
  updateWelcomeContent,
  resetWelcomeContent,
  getMessageContent,
  updateMessageContent,
  resetMessageContent,
  getPurposesContent,
  updatePurposesContent,
  resetPurposesContent,
  getPastoralTeamContent,
  updatePastoralTeamContent,
  resetPastoralTeamContent,
  getMinistriesPresentationContent,
  updateMinistriesPresentationContent,
  resetMinistriesPresentationContent,
  getServicesBannerContent,
  updateServicesBannerContent,
  resetServicesBannerContent,
  getLocalGatheringsContent,
  updateLocalGatheringsContent,
  resetLocalGatheringsContent,
  getLocalGatheringOptions,
  updateLocalGatheringOptions,
  resetLocalGatheringOptions,
  getGalleryContent,
  updateGalleryContent,
  resetGalleryContent,
  getSocialMediaContent,
  updateSocialMediaContent,
  resetSocialMediaContent,
  getDonationsContent,
  updateDonationsContent,
  resetDonationsContent,
  getLocationsContent,
  updateLocationsContent,
  resetLocationsContent,
  getGoogleMapsConfig,
  updateGoogleMapsConfig,
  resetGoogleMapsConfig,
  getIfthenpayConfig,
  updateIfthenpayConfig,
  resetIfthenpayConfig,
} from '../services/api'

// ─── Auth state ───────────────────────────────────────────────────────────────
const isAuthenticated = ref(checkIsAuthenticated())
const username = ref('')
const password = ref('')
const isLoggingIn = ref(false)

// ─── App state ────────────────────────────────────────────────────────────────
const isLoadingData = ref(false)
const isSaving = ref(false)
const isInitialLoading = ref(true)
const initialSnapshot = ref(null)
const error = ref('')
const success = ref('')

let feedbackTimer = null
function showFeedback(type, message) {
  if (feedbackTimer) clearTimeout(feedbackTimer)
  if (type === 'success') {
    success.value = message
    error.value = ''
  } else {
    error.value = message
    success.value = ''
  }
  feedbackTimer = setTimeout(() => {
    success.value = ''
    error.value = ''
  }, 4500)
}

function handleBeforeUnload(e) {
  if (hasUnsavedChanges.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}

onMounted(async () => {
  window.addEventListener('beforeunload', handleBeforeUnload)
  if (isAuthenticated.value) {
    await loadAdminData()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
  if (feedbackTimer) clearTimeout(feedbackTimer)
})

// ─── Section visibility refs ──────────────────────────────────────────────────
const openSections = ref({
  welcome: false,
  message: false,
  purposes: false,
  pastoralTeam: false,
  ministries: false,
  servicesBanner: false,
  localGatherings: false,
  localGatheringOptions: false,
  gallery: false,
  socialMedia: false,
  donations: false,
  locations: false,
})

function toggleSection(section) {
  openSections.value[section] = !openSections.value[section]
}
function openAllSections() {
  Object.keys(openSections.value).forEach(k => openSections.value[k] = true)
}
function closeAllSections() {
  Object.keys(openSections.value).forEach(k => openSections.value[k] = false)
}

// ─── Section data refs ────────────────────────────────────────────────────────
const infoContent = ref('')
const messageContent = ref('')
const purposes = ref([])
const pastoralTeam = ref([])
const ministries = ref([])
const servicesBannerContent = ref('')
const localGatheringsData = ref({
  localGatheringsQuote: '',
  localGatheringsQuoteReference: '',
  localGatheringsBody: '',
})
const localGatheringOptions = ref([])
const galleryImages = ref([])
const socialMedia = ref([])
const donationsData = ref({
  donationsBody: '',
  donationsQuote: '',
  donationsQuoteAuthor: '',
  beneficiary: 'Igreja Cristã Manancial de Águas Vivas',
  iban: 'PT50 0007 0246 0014 0750 0033 4',
  bank: 'NOVO BANCO, SA',
  bic: 'BESCPTPLXXX',
  treasuryEmail: 'tesouraria.icmav@gmail.com',
  categories: [
    { id: 'Ofertas', name: 'Ofertas' },
    { id: 'Dízimos', name: 'Dízimos' },
    { id: 'Missões', name: 'Missões' },
  ],
})
const locations = ref([])
const googleMapsConfig = ref({
  apiKey: '',
  mapId: '',
})
const sibsConfig = ref({
  api_base: 'https://api.ifthenpay.com/spg/payment',
  mbway_key: '',
  default_email: '',
})

function serializeAdminState() {
  return JSON.stringify({
    infoContent: infoContent.value,
    messageContent: messageContent.value,
    purposes: purposes.value,
    pastoralTeam: pastoralTeam.value,
    ministries: ministries.value,
    servicesBannerContent: servicesBannerContent.value,
    localGatheringsData: localGatheringsData.value,
    localGatheringOptions: localGatheringOptions.value,
    galleryImages: galleryImages.value,
    socialMedia: socialMedia.value,
    donationsData: donationsData.value,
    locations: locations.value,
    googleMapsConfig: googleMapsConfig.value,
    sibsConfig: sibsConfig.value,
  })
}

const hasUnsavedChanges = computed(() => {
  if (isInitialLoading.value || !initialSnapshot.value) return false
  return serializeAdminState() !== initialSnapshot.value
})

function handleNotification({ type, message }) {
  showFeedback(type, message)
}

// ─── Data loading ─────────────────────────────────────────────────────────────
async function loadAdminData() {
  isLoadingData.value = true
  isInitialLoading.value = true
  error.value = ''
  try {
    const [
      welcomeRes, messageRes, purposesRes, pastoralRes,
      ministriesRes, servicesRes, lgContentRes, lgOptionsRes,
      galleryRes, socialRes, donationsRes, locationsRes, mapsRes, sibsRes,
    ] = await Promise.all([
      getWelcomeContent(),
      getMessageContent(),
      getPurposesContent(),
      getPastoralTeamContent(),
      getMinistriesPresentationContent(),
      getServicesBannerContent(),
      getLocalGatheringsContent(),
      getLocalGatheringOptions(),
      getGalleryContent(),
      getSocialMediaContent(),
      getDonationsContent(),
      getLocationsContent(),
      getGoogleMapsConfig().catch(() => ({ value: {} })),
      getIfthenpayConfig().catch(() => ({ value: {} })),
    ])

    infoContent.value = welcomeRes.value ?? ''
    messageContent.value = messageRes.value ?? ''
    purposes.value = Array.isArray(purposesRes.value) ? purposesRes.value : []
    pastoralTeam.value = Array.isArray(pastoralRes.value) ? pastoralRes.value : []
    ministries.value = Array.isArray(ministriesRes.value) ? ministriesRes.value : []
    servicesBannerContent.value = servicesRes.value ?? ''

    const lgv = lgContentRes.value
    localGatheringsData.value = lgv && typeof lgv === 'object' ? lgv : {
      localGatheringsQuote: '',
      localGatheringsQuoteReference: '',
      localGatheringsBody: '',
    }

    localGatheringOptions.value = Array.isArray(lgOptionsRes.value) ? lgOptionsRes.value : []
    galleryImages.value = Array.isArray(galleryRes.value) ? galleryRes.value : []
    socialMedia.value = Array.isArray(socialRes.value) ? socialRes.value : []

    const dv = donationsRes.value
    if (dv && typeof dv === 'object') {
      donationsData.value = {
        donationsBody: dv.donationsBody ?? '',
        donationsQuote: dv.donationsQuote ?? '',
        donationsQuoteAuthor: dv.donationsQuoteAuthor ?? dv.donationsQuoteReference ?? '',
        beneficiary: dv.beneficiary ?? 'Igreja Cristã Manancial de Águas Vivas',
        iban: dv.iban ?? 'PT50 0007 0246 0014 0750 0033 4',
        bank: dv.bank ?? 'NOVO BANCO, SA',
        bic: dv.bic ?? 'BESCPTPLXXX',
        treasuryEmail: dv.treasuryEmail ?? 'tesouraria.icmav@gmail.com',
        categories: Array.isArray(dv.categories) ? dv.categories : [
          { id: 'Ofertas', name: 'Ofertas' },
          { id: 'Dízimos', name: 'Dízimos' },
          { id: 'Missões', name: 'Missões' },
        ],
      }
    }

    locations.value = Array.isArray(locationsRes.value) ? locationsRes.value : []

    const gmv = mapsRes?.value
    googleMapsConfig.value = gmv && typeof gmv === 'object' ? {
      apiKey: gmv.apiKey ?? gmv.api_key ?? '',
      mapId: gmv.mapId ?? gmv.map_id ?? '',
    } : {
      apiKey: '',
      mapId: '',
    }

    const sv = sibsRes.value
    sibsConfig.value = sv && typeof sv === 'object' ? {
      api_base: sv.api_base ?? sv.sibs_api_base ?? 'https://api.ifthenpay.com/spg/payment',
      mbway_key: sv.mbway_key ?? sv.sibs_client_id ?? '',
      default_email: sv.default_email ?? '',
    } : {
      api_base: 'https://api.ifthenpay.com/spg/payment',
      mbway_key: '',
      default_email: '',
    }

  } catch (err) {
    showFeedback('error', err.message || 'Erro ao carregar dados')
    if (err.message && err.message.includes('Sessão expirada')) {
      isAuthenticated.value = false
    }
  } finally {
    isLoadingData.value = false
  }

  await nextTick()
  await new Promise(resolve => setTimeout(resolve, 60))
  initialSnapshot.value = serializeAdminState()
  isInitialLoading.value = false
}

// ─── Auth actions ─────────────────────────────────────────────────────────────
async function handleLogin() {
  error.value = ''
  success.value = ''
  isLoggingIn.value = true
  try {
    await adminLogin(username.value, password.value)
    isAuthenticated.value = true
    await loadAdminData()
  } catch (err) {
    showFeedback('error', err.message || 'Credenciais inválidas')
  } finally {
    isLoggingIn.value = false
  }
}

function handleLogout() {
  clearAuthToken()
  isAuthenticated.value = false
  initialSnapshot.value = null
  username.value = ''
  password.value = ''
  error.value = ''
  success.value = ''
}

// ─── Save All ─────────────────────────────────────────────────────────────────
async function handleSave() {
  isSaving.value = true
  error.value = ''
  success.value = ''
  try {
    await Promise.all([
      updateWelcomeContent(infoContent.value),
      updateMessageContent(messageContent.value),
      updatePurposesContent(purposes.value),
      updatePastoralTeamContent(pastoralTeam.value),
      updateMinistriesPresentationContent(ministries.value),
      updateServicesBannerContent(servicesBannerContent.value),
      updateLocalGatheringsContent(localGatheringsData.value),
      updateLocalGatheringOptions(localGatheringOptions.value),
      updateGalleryContent(galleryImages.value),
      updateSocialMediaContent(socialMedia.value),
      updateDonationsContent(donationsData.value),
      updateLocationsContent(locations.value),
      updateGoogleMapsConfig(googleMapsConfig.value),
      updateIfthenpayConfig(sibsConfig.value),
    ])

    initialSnapshot.value = serializeAdminState()
    showFeedback('success', 'Todo o conteúdo foi guardado com sucesso.')
  } catch (err) {
    showFeedback('error', err.message || 'Erro ao guardar conteúdos')
  } finally {
    isSaving.value = false
  }
}

// ─── Reset Handlers ───────────────────────────────────────────────────────────
async function handleResetWelcome() {
  try {
    const data = await resetWelcomeContent()
    infoContent.value = data.value
    showFeedback('success', 'Conteúdo Info reposto.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor conteúdo Info') }
}

async function handleResetMessage() {
  try {
    const data = await resetMessageContent()
    messageContent.value = data.value
    showFeedback('success', 'Conteúdo Message reposto.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor conteúdo Message') }
}

async function handleResetPurposes() {
  try {
    const data = await resetPurposesContent()
    purposes.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Propósitos repostos.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor propósitos') }
}

async function handleResetPastoralTeam() {
  try {
    const data = await resetPastoralTeamContent()
    pastoralTeam.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Equipa pastoral reposta.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor equipa pastoral') }
}

async function handleResetMinistriesPresentation() {
  try {
    const data = await resetMinistriesPresentationContent()
    ministries.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Ministérios repostos.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor ministérios') }
}

async function handleResetServicesBanner() {
  try {
    const data = await resetServicesBannerContent()
    servicesBannerContent.value = data.value
    showFeedback('success', 'Serviços Banner reposto.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Serviços Banner') }
}

async function handleResetLocalGatherings() {
  try {
    const data = await resetLocalGatheringsContent()
    const v = data.value
    localGatheringsData.value = v && typeof v === 'object' ? v : {
      localGatheringsQuote: '', localGatheringsQuoteReference: '', localGatheringsBody: '',
    }
    showFeedback('success', 'Encontros Locais repostos.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Encontros Locais') }
}

async function handleResetLocalGatheringOptions() {
  try {
    const data = await resetLocalGatheringOptions()
    localGatheringOptions.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Pequenos Grupos repostos.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Pequenos Grupos') }
}

async function handleResetGallery() {
  try {
    const data = await resetGalleryContent()
    galleryImages.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Galeria reposta.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Galeria') }
}

async function handleResetSocialMedia() {
  try {
    const data = await resetSocialMediaContent()
    socialMedia.value = Array.isArray(data.value) ? data.value : []
    showFeedback('success', 'Redes Sociais repostas.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Redes Sociais') }
}

async function handleResetDonations() {
  try {
    const [donationsRes, sibsRes] = await Promise.all([
      resetDonationsContent(),
      resetIfthenpayConfig(),
    ])

    const dv = donationsRes.value
    if (dv && typeof dv === 'object') {
      donationsData.value = {
        donationsBody: dv.donationsBody ?? '',
        donationsQuote: dv.donationsQuote ?? '',
        donationsQuoteAuthor: dv.donationsQuoteAuthor ?? dv.donationsQuoteReference ?? '',
        beneficiary: dv.beneficiary ?? 'Igreja Cristã Manancial de Águas Vivas',
        iban: dv.iban ?? 'PT50 0007 0246 0014 0750 0033 4',
        bank: dv.bank ?? 'NOVO BANCO, SA',
        bic: dv.bic ?? 'BESCPTPLXXX',
        treasuryEmail: dv.treasuryEmail ?? 'tesouraria.icmav@gmail.com',
        categories: Array.isArray(dv.categories) ? dv.categories : [
          { id: 'Ofertas', name: 'Ofertas' },
          { id: 'Dízimos', name: 'Dízimos' },
          { id: 'Missões', name: 'Missões' },
        ],
      }
    }

    const sv = sibsRes.value
    sibsConfig.value = sv && typeof sv === 'object' ? {
      api_base: sv.api_base ?? sv.sibs_api_base ?? 'https://api.ifthenpay.com/spg/payment',
      mbway_key: sv.mbway_key ?? sv.sibs_client_id ?? '',
      default_email: sv.default_email ?? '',
    } : {
      api_base: 'https://api.ifthenpay.com/spg/payment',
      mbway_key: '',
      default_email: '',
    }

    showFeedback('success', 'Contribuições e Gateway IFTHENPAY repostas.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Contribuições') }
}

async function handleResetLocations() {
  try {
    const [locationsRes, mapsRes] = await Promise.all([
      resetLocationsContent(),
      resetGoogleMapsConfig(),
    ])
    locations.value = Array.isArray(locationsRes.value) ? locationsRes.value : []
    const gmv = mapsRes?.value
    googleMapsConfig.value = gmv && typeof gmv === 'object' ? {
      apiKey: gmv.apiKey ?? gmv.api_key ?? '',
      mapId: gmv.mapId ?? gmv.map_id ?? '',
    } : {
      apiKey: '',
      mapId: '',
    }
    showFeedback('success', 'Localizações e Configuração Google Maps repostas.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor Localizações') }
}

async function handleResetSibsConfig() {
  try {
    const data = await resetIfthenpayConfig()
    const sv = data.value
    sibsConfig.value = sv && typeof sv === 'object' ? {
      api_base: sv.api_base ?? sv.sibs_api_base ?? 'https://api.ifthenpay.com/spg/payment',
      mbway_key: sv.mbway_key ?? sv.sibs_client_id ?? '',
      default_email: sv.default_email ?? '',
    } : {
      api_base: 'https://api.ifthenpay.com/spg/payment',
      mbway_key: '',
      default_email: '',
    }
    showFeedback('success', 'Configuração IFTHENPAY reposta.')
  } catch (err) { showFeedback('error', err.message || 'Erro ao repor configuração IFTHENPAY') }
}
</script>

<style scoped>
.admin-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 1.5rem 5rem;
  background: #f3f4f6;
  width: 100%;
}

.admin-card {
  width: 100%;
  max-width: 1280px;
  background: #fff;
  border-radius: 16px;
  padding: 2rem 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: relative;
  z-index: 10;
}

.login-card {
  max-width: 420px;
  margin-top: 4rem;
  display: grid;
  gap: 1rem;
}

.global-actions {
  display: flex;
  gap: 1rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #e5e7eb;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 1.25rem;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.unsaved-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #fef3c7;
  color: #b45309;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid #fde68a;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.75; }
}

.alert-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem 1.25rem;
  border-radius: 10px;
  font-size: 0.925rem;
  font-weight: 500;
}

.alert-success {
  background: #ecfdf3;
  color: #027a48;
  border: 1px solid #a6f4c5;
}

.alert-error {
  background: #fef3f2;
  color: #b42318;
  border: 1px solid #fecdca;
}

.alert-close {
  background: transparent;
  border: none;
  font-size: 1.4rem;
  line-height: 1;
  color: inherit;
  padding: 0 0.25rem;
  cursor: pointer;
  opacity: 0.6;
  border-radius: 4px;
}

.alert-close:hover {
  opacity: 1;
}

h1 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.loading-state {
  padding: 3rem;
  text-align: center;
  color: #6b7280;
  font-size: 1.1rem;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 0.5rem;
}

input {
  font: inherit;
  padding: 0.7rem 0.9rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  width: 100%;
  background: #fafafa;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: #fff;
}

button {
  cursor: pointer;
  border: none;
  background: #6366f1;
  color: #fff;
  font-weight: 600;
  white-space: nowrap;
  padding: 0.7rem 1.2rem;
  border-radius: 8px;
  transition: opacity 0.15s;
}

button:hover:not(:disabled) {
  opacity: 0.85;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.secondary-btn {
  background: #eef2ff;
  color: #3730a3;
}

.save-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e5e7eb;
}

.save-btn {
  padding: 0.85rem 2.5rem;
  font-size: 1rem;
  border-radius: 10px;
}

.error {
  color: #b42318;
  font-weight: 500;
}

.success {
  color: #027a48;
  font-weight: 500;
}
</style>