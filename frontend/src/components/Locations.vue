<!-- src/components/Locations.vue -->

<template>
  <section id="locations" class="relative w-full" data-aos="fade-up">
    <div v-if="loading" class="text-center py-12 text-gray-500">
      A carregar localizações...
    </div>

    <div v-else-if="error" class="text-center py-12 text-red-600">
      {{ error }}
    </div>

    <div v-else-if="current" class="relative min-h-[800px] overflow-hidden">
      <div ref="mapEl" class="absolute inset-0 w-full h-full"></div>

      <div class="absolute inset-0 bg-slate-950/05 pointer-events-none"></div>
      
      <!-- Vinheta em Mobile: suave apenas no topo para leitura do cabeçalho -->
      <div class="lg:hidden absolute top-0 inset-x-0 h-64 sm:h-72 bg-gradient-to-b from-slate-950/80 via-slate-950/35 to-transparent pointer-events-none"></div>
      
      <!-- Vinheta em Desktop: gradiente lateral original intacto -->
      <div class="hidden lg:block absolute inset-0 bg-gradient-to-r from-slate-950/80 via-slate-950/15 to-slate-950/00 pointer-events-none"></div>

      <div class="relative z-10 h-full pointer-events-none">
        <div class="max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-8 md:py-12">
          <div class="max-w-xl pointer-events-auto">
            <p class="text-2xl md:text-4xl uppercase tracking-[0.11em] text-white mb-6">
              Onde estamos
            </p>

            <!-- Abas com scroll horizontal sem qualquer barra de scroll visível -->
            <div class="flex overflow-x-auto md:flex-wrap gap-2.5 sm:gap-3 pb-2 md:pb-3 mb-4 md:mb-6 flex-nowrap md:flex-wrap -mx-4 px-4 md:mx-0 md:px-0 hide-horizontal-scrollbar">
              <button
                v-for="(location, i) in locations"
                :key="location.slug"
                type="button"
                @click="handleSelectLocation(i)"
                class="shrink-0 rounded-full px-5 py-2.5 text-sm md:text-base font-semibold transition-all duration-300 ease-out backdrop-blur-sm cursor-pointer whitespace-nowrap"
                :class="
                  selectedIndex === i
                    ? 'bg-white text-primary shadow-lg'
                    : 'bg-white/15 text-white border border-white/20 hover:bg-white/25'
                "
              >
                {{ location.name }}
              </button>
            </div>

            <!-- Wrapper do Cartão e Chevron com topo perfeitamente alinhado -->
            <div class="relative">
              <!-- Botão Chevron na margem esquerda (alinhado ao topo do cartão) -->
              <button
                v-if="!isCardExpanded"
                type="button"
                @click="isCardExpanded = true"
                class="lg:hidden absolute top-0 -left-4 z-30 w-11 h-14 bg-white/95 backdrop-blur-md rounded-r-2xl shadow-2xl flex flex-col items-center justify-center text-primary font-bold border-y border-r border-white/80 cursor-pointer transition-transform hover:scale-105"
                aria-label="Mostrar cartão de localização"
              >
                <i class="fa-solid fa-chevron-right text-lg"></i>
                <span class="text-[9px] uppercase tracking-tighter mt-0.5 text-gray-500 font-semibold">
                  Info
                </span>
              </button>

              <!-- Cartão com comportamento retrátil 100% escondido em mobile e fixo em desktop -->
              <div
                class="relative transition-transform duration-300 ease-out"
                :class="[
                  isCardExpanded
                    ? 'translate-x-0'
                    : '-translate-x-[120%] lg:translate-x-0'
                ]"
              >
                <div class="bg-white/90 backdrop-blur-md rounded-[1.75rem] shadow-xl p-6 md:p-8 border border-white/60">
                  <div class="flex items-center justify-between mb-2">
                    <p class="text uppercase tracking-[0.22em] text-gray-500">
                      Localização
                    </p>
                    <button
                      type="button"
                      @click="isCardExpanded = false"
                      class="lg:hidden text-gray-500 hover:text-gray-800 text-xs font-semibold p-1 cursor-pointer flex items-center gap-1"
                    >
                      <i class="fa-solid fa-chevron-left"></i> Recolher
                    </button>
                  </div>

                  <h3 class="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                    {{ current.name }}
                  </h3>

                <div class="space-y-4">
                  <div class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-church text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">Tipo de localização</p>
                      <p class="text-lg text-gray-900">{{ current.type }}</p>
                    </div>
                  </div>

                  <div class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-calendar-alt text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">Culto de Domingo</p>
                      <p class="text-lg text-gray-900">{{ current.sundayService }}</p>
                    </div>
                  </div>

                  <div class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-envelope text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">E-mail</p>
                      <a :href="`mailto:${current.email}`" class="text-primary underline break-all">
                        {{ current.email }}
                      </a>
                    </div>
                  </div>

                  <div class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-phone text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">Telefone</p>
                      <a :href="`tel:${current.phone}`" class="text-primary underline">
                        {{ current.phone }}
                      </a>
                    </div>
                  </div>

                  <div class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-map-marker-alt text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">Morada</p>

                      <a
                        v-if="current.mapsLink"
                        :href="current.mapsLink"
                        class="text-primary underline cursor-pointer"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {{ current.address }}
                      </a>

                      <p v-else class="text-gray-900">
                        {{ current.address }}
                      </p>
                    </div>
                  </div>

                  <div v-if="current.customWebsite" class="flex items-center gap-3">
                    <i class="text-xl fa-solid fa-globe text-primary"></i>
                    <div>
                      <p class="text-xs uppercase tracking-wider text-gray-500">Site dedicado</p>
                      <a
                        :href="normalizeWebsiteUrl(current.customWebsite)"
                        class="text-primary underline"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {{ current.customWebsite }}
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    <div v-else class="text-center py-12 text-gray-500">
      Sem localizações disponíveis.
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { getLocationsContent, getGoogleMapsConfig } from '../services/api'

const envApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || ''
const envMapId = import.meta.env.VITE_GOOGLE_MAP_ID || ''

const googleMapsApiKey = ref(envApiKey)
const googleMapsMapId = ref(envMapId)

const locations = ref([])
const loading = ref(true)
const error = ref('')
const selectedIndex = ref(0)
const isCardExpanded = ref(false)
const mapEl = ref(null)

function handleSelectLocation(index) {
  selectedIndex.value = index
}

function toggleMobileCard() {
  isCardExpanded.value = !isCardExpanded.value
}

let map = null
let marker = null
let googleMapsPromise = null
let AdvancedMarkerElementClass = null

const current = computed(() => locations.value[selectedIndex.value] || null)

function parseLatLng(value) {
  if (!value || typeof value !== 'string') return null
  const [lat, lng] = value.split(',').map(v => Number(v.trim()))
  if (Number.isNaN(lat) || Number.isNaN(lng)) return null
  return { lat, lng }
}

function loadGoogleMapsScript() {
  if (window.google?.maps) return Promise.resolve(window.google.maps)

  if (!googleMapsApiKey.value) {
    return Promise.reject(new Error('Chave da API do Google Maps não definida'))
  }

  if (googleMapsPromise) return googleMapsPromise

  googleMapsPromise = new Promise((resolve, reject) => {
    const callbackName = '__initGoogleMaps'
    const existingScript = document.querySelector('script[data-google-maps="true"]')

    window[callbackName] = () => {
      resolve(window.google.maps)
      delete window[callbackName]
    }

    if (existingScript) return

    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(googleMapsApiKey.value)}&loading=async&callback=${callbackName}&libraries=marker`
    script.async = true
    script.defer = true
    script.dataset.googleMaps = 'true'
    script.onerror = () => {
      reject(new Error('Erro ao carregar Google Maps'))
      delete window[callbackName]
    }

    document.head.appendChild(script)
  })

  return googleMapsPromise
}

async function ensureMarkerLibrary() {
  try {
    await loadGoogleMapsScript()

    if (!AdvancedMarkerElementClass && window.google?.maps?.importLibrary) {
      const { AdvancedMarkerElement } = await window.google.maps.importLibrary('marker')
      AdvancedMarkerElementClass = AdvancedMarkerElement
    }
  } catch (err) {
    console.warn('Google Maps marker library could not be loaded:', err)
  }
}

function getEffectiveCenter() {
  if (!current.value) return null
  const mapCenter = parseLatLng(current.value.mapCenter)
  const markerPos = parseLatLng(current.value.markerPosition)

  const isMobile = typeof window !== 'undefined' && window.innerWidth < 1024

  if (isMobile) {
    // No mobile (< 1024px), aplicamos uma ligeira compensação (~3% para a direita)
    // para um enquadramento mais natural
    if (markerPos && mapCenter) {
      return {
        lat: markerPos.lat + (mapCenter.lat - markerPos.lat) * 0.15,
        lng: markerPos.lng + (mapCenter.lng - markerPos.lng) * 0.15,
      }
    }
    if (markerPos) return markerPos
    return mapCenter
  }

  // Em desktop, usa o centro original configurado
  return mapCenter || markerPos
}

async function initMap() {
  if (!mapEl.value || !current.value || !googleMapsApiKey.value) return

  try {
    await ensureMarkerLibrary()

    if (!window.google?.maps?.Map) return

    const center = getEffectiveCenter()
    const markerPosition = parseLatLng(current.value.markerPosition) || center
    const zoom = Number.isInteger(current.value.mapZoom) ? current.value.mapZoom : 14

    if (!center) return

    map = new window.google.maps.Map(mapEl.value, {
      center,
      zoom,
      mapId: googleMapsMapId.value || undefined,
      gestureHandling: 'none',
      zoomControl: true,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
      rotateControl: false,
      scaleControl: false,
      clickableIcons: false,
    })

    if (markerPosition && AdvancedMarkerElementClass) {
      marker = new AdvancedMarkerElementClass({
        map,
        position: markerPosition,
        title: current.value.name,
      })
    }
  } catch (err) {
    console.warn('Google Maps initialization failed:', err)
  }
}

function updateMap() {
  if (!map || !current.value) return

  try {
    const center = getEffectiveCenter()
    const markerPosition = parseLatLng(current.value.markerPosition) || center
    const zoom = Number.isInteger(current.value.mapZoom) ? current.value.mapZoom : 14

    if (!center) return

    if (typeof map.setCenter === 'function') {
      map.setCenter(center)
      map.setZoom(zoom)
    }

    if (marker && markerPosition) {
      marker.position = markerPosition
      marker.title = current.value.name
      marker.map = map
    }
  } catch (err) {
    console.warn('Map update skipped:', err)
  }
}

async function loadLocations() {
  loading.value = true
  error.value = ''

  try {
    const [locationsRes, mapsRes] = await Promise.all([
      getLocationsContent(),
      getGoogleMapsConfig().catch(() => ({ value: {} })),
    ])

    locations.value = Array.isArray(locationsRes?.value) ? locationsRes.value : []

    const dbKey = mapsRes?.value?.apiKey
    const dbMapId = mapsRes?.value?.mapId
    if (dbKey) {
      googleMapsApiKey.value = dbKey
    }
    if (dbMapId) {
      googleMapsMapId.value = dbMapId
    }

    selectedIndex.value = 0
  } catch (err) {
    error.value = err.message || 'Erro ao carregar Localizações'
    locations.value = []
  } finally {
    loading.value = false
  }
}

function normalizeWebsiteUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  return `https://${url}`
}

let resizeTimer = null
function handleResize() {
  clearTimeout(resizeTimer)
  resizeTimer = setTimeout(() => {
    if (map) updateMap()
  }, 150)
}

watch(
  [current, mapEl, loading, googleMapsApiKey],
  async ([newCurrent, newMapEl, isLoading, newApiKey]) => {
    if (isLoading || !newCurrent || !newMapEl || !newApiKey) return

    await nextTick()

    if (!map) {
      await initMap()
    } else {
      updateMap()
    }
  },
  { immediate: true }
)

onMounted(() => {
  loadLocations()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.hide-horizontal-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-horizontal-scrollbar::-webkit-scrollbar {
  display: none;
  width: 0;
  height: 0;
}
</style>
