<!-- src/components/PastoralTeam.vue -->
 
<template>
  <div data-aos="fade-up">
    <div v-if="loading" class="text-center py-8 text-gray-500">
      A carregar equipa pastoral...
    </div>

    <div v-else-if="error" class="text-center py-8 text-red-600">
      {{ error }}
    </div>

    <template v-else>
    
      <!-- Lead Pastors -->
      <div class="relative z-20 mb-2">
        <div 
          class="relative flex justify-center items-start py-4"
          @mouseleave="hoveredLeadPastor = null"
        >
          <button
            v-for="(p, i) in leadPastors"
            :key="p.id"
            type="button"
            @click="toggleLeadBio(p.id)"
            @mouseenter="hoveredLeadPastor = i"
            class="relative cursor-pointer transition-all duration-300 ease-out"
            :class="[
              i === 1 ? '-ml-6' : '',
              activeLeadId === p.id ? 'z-30' : 'z-10',
              activeLeadId && activeLeadId !== p.id
                ? 'opacity-65 saturate-80 scale-[0.96]'
                : 'opacity-100 saturate-100 scale-100'
            ]"
          >
            <div
              class="flex flex-col items-center origin-bottom transform-gpu transition-all duration-300 ease-out"
              :class="getLeadPastorDockScale(i)"
            >
              <p class="mb-2 text-center font-semibold whitespace-pre-line">
                {{ p.name }}
              </p>

              <div class="w-48 h-48 rounded-full overflow-hidden shadow-lg">
                <img
                  :src="resolvePhotoUrl(p.photo)"
                  :alt="p.name"
                  loading="lazy"
                  decoding="async"
                  class="object-cover w-full h-full"
                />
              </div>
            </div>
          </button>
        </div>

        <transition name="slide-fade">
          <div
            v-if="activeLeadPastor"
            class="relative z-20 max-w-6xl mx-auto -mt-20 pt-20 bg-base-100 border border-gray-200 rounded-2xl shadow-lg px-8 pb-8"
          >
            <h3 class="text-2xl font-bold text-left mt-2 mb-6 whitespace-normal">
              {{ activeLeadPastor.name }}
            </h3>

            <div
              class="pastor-bio text-gray-700 text-left max-w-none"
              v-html="activeLeadPastor.bio"
            ></div>
          </div>
        </transition>
      </div>

      <!-- Message -->
      <div
        v-if="messageContent"
        class="relative text-lg text-center max-w-5xl mx-auto px-6 py-8 bg-base-100 border border-gray-200 rounded-lg shadow-sm"
      >
        <div
          class="message-content text-center max-w-none"
          v-html="messageContent"
        ></div>
      </div>

      <!-- Other Pastors -->
      <div class="relative mt-2">
        <div
          ref="scrollContainer"
          class="overflow-x-auto overflow-y-hidden scroll-smooth hide-scrollbar py-8 px-8"
          @scroll="checkArrows"
        >
          <div
            class="flex w-max min-w-full gap-10"
            @mouseleave="hoveredOtherPastor = null"
          >
            <div
              v-for="(p, i) in otherPastors"
              :key="p.id"
              @click="toggleOtherBio(p.id)"
              @mouseenter="hoveredOtherPastor = i"
              class="flex-shrink-0 w-36 cursor-pointer relative transition-all duration-300 ease-out"
              :class="[
                i === 0 ? 'ml-auto' : '',
                i === otherPastors.length - 1 ? 'mr-auto' : '',
                activeOtherPastor?.id === p.id ? 'z-30' : 'z-10',
                activeOtherPastor && activeOtherPastor.id !== p.id
                  ? 'opacity-65 saturate-80 scale-[0.88]'
                  : 'opacity-100 saturate-100 scale-100'
              ]"
              :style="{
                marginRight:
                  (otherPastors[i + 1] && otherPastors[i + 1].spouseId === p.id)
                    ? '-3.5rem'
                    : undefined
              }"
            >
              <div
                class="flex flex-col items-center origin-bottom transform-gpu transition-all duration-300 ease-out"
                :class="getOtherPastorDockScale(i)"
              >
                <div class="w-36 h-36 rounded-full overflow-hidden shadow-lg">
                  <img :src="resolvePhotoUrl(p.photo)" :alt="p.name" loading="lazy" decoding="async" class="object-cover w-full h-full" />
                </div>

                <p
                  class="mt-2 text-center font-medium whitespace-pre-line transition-opacity duration-200"
                  :class="activeOtherPastor?.id === p.id ? 'opacity-0' : 'opacity-100'"
                >
                  {{ p.name }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <button
          v-if="showLeftArrow"
          class="absolute left-2 top-1/2 -translate-y-1/2 rounded-full p-2 z-10"
          @click="scrollLeft"
        >
          <i class="fas fa-chevron-left text-xl text-gray-200"></i>
        </button>

        <button
          v-if="showRightArrow"
          class="absolute right-2 top-1/2 -translate-y-1/2 rounded-full p-2 z-10"
          @click="scrollRight"
        >
          <i class="fas fa-chevron-right text-xl text-gray-200"></i>
        </button>
      </div>

      <div
        v-if="activeOtherPastor"
        class="relative z-20 max-w-7xl mx-auto -mt-[9rem] pt-20 bg-base-100 border border-gray-200 rounded-2xl shadow-lg px-8 pb-8"
      >
        <transition name="slide-fade" mode="out-in">
          <div :key="activeOtherPastor.id">
            <h3 class="text-2xl font-bold text-left mb-6 whitespace-normal">
              {{ activeOtherPastor.name }}
            </h3>

            <div
              class="pastor-bio text-gray-700 text-left max-w-none"
              v-html="activeOtherPastor.bio"
            ></div>
          </div>
        </transition>
      </div>
    </template>
  </div>
</template>
  
<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { getPastoralTeamContent, getMessageContent } from '../services/api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const BACKEND_BASE_URL = API_BASE_URL.replace('/api', '')
const pastors = ref([])
const loading = ref(true)
const error = ref('')
const messageContent = ref('')

// dropdown state
const activeLeadId = ref(null)
const activeOtherId = ref(null)
const hoveredLeadPastor = ref(null)
const hoveredOtherPastor = ref(null)

function getLeadPastorDockScale(i) {
  if (hoveredLeadPastor.value === null) return 'scale-100'

  const distance = Math.abs(hoveredLeadPastor.value - i)

  if (distance === 0) return 'scale-[1.10]'
  if (distance === 1) return 'scale-[1.00]'
  if (distance === 2) return 'scale-[1.00]'
  return 'scale-100'
}

function getOtherPastorDockScale(i) {
  if (hoveredOtherPastor.value === null) return 'scale-100'

  const distance = Math.abs(hoveredOtherPastor.value - i)

  if (distance === 0) return 'scale-[1.10]'
  if (distance === 1) return 'scale-[1.00]'
  if (distance === 2) return 'scale-[1.00]'
  return 'scale-100'
}

function toggleLeadBio(id) {
  if (activeLeadId.value === id) {
    activeLeadId.value = null
    hoveredLeadPastor.value = null
  } else {
    activeLeadId.value = id
    activeOtherId.value = null
  }
}

function toggleOtherBio(id) {
  if (activeOtherId.value === id) {
    activeOtherId.value = null
    hoveredOtherPastor.value = null
  } else {
    activeOtherId.value = id
    activeLeadId.value = null
  }
}

const activeLeadPastor = computed(() =>
  leadPastors.value.find(p => p.id === activeLeadId.value)
)

const activeOtherPastor = computed(() =>
  otherPastors.value.find(p => p.id === activeOtherId.value)
)

const leadPastors = computed(() =>
  pastors.value.filter(p => p.isLeadPair)
)

const otherPastors = computed(() =>
  pastors.value.filter(p => !p.isLeadPair)
)

async function loadPastoralTeam() {
  loading.value = true
  error.value = ''

  try {
    const data = await getPastoralTeamContent()
    pastors.value = Array.isArray(data.value) ? data.value : []
  } catch (err) {
    error.value = err.message || 'Erro ao carregar equipa pastoral'
    pastors.value = []
  } finally {
    loading.value = false
    setTimeout(checkArrows, 0)
  }
}

// scrolling & arrows
const scrollContainer = ref(null)
const showLeftArrow = ref(false)
const showRightArrow = ref(false)

function checkArrows() {
  const el = scrollContainer.value
  if (!el) return

  showLeftArrow.value = el.scrollLeft > 10
  showRightArrow.value = el.scrollLeft + el.clientWidth + 10 < el.scrollWidth
}

function scrollLeft() {
  scrollContainer.value?.scrollBy({ left: -200, behavior: 'smooth' })
}

function scrollRight() {
  scrollContainer.value?.scrollBy({ left: 200, behavior: 'smooth' })
}

onMounted(async () => {
  await Promise.all([
    loadPastoralTeam(),
    loadMessage()
  ])
  checkArrows()
  window.addEventListener('resize', checkArrows)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkArrows)
})

function resolvePhotoUrl(photo) {
  if (!photo) return ''

  if (photo.startsWith('http://') || photo.startsWith('https://')) {
    return photo
  }

  if (photo.startsWith('/uploads/')) {
    return `${BACKEND_BASE_URL}${photo}`
  }

  if (photo.startsWith('/src/assets/')) {
    return photo.replace('/src/assets/', '/')
  }

  return photo
}

async function loadMessage() {
  try {
    const data = await getMessageContent()
    messageContent.value = data?.value || ''
  } catch (err) {
    messageContent.value = ''
  }
}
</script>
  
<style scoped>
.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.pastor-bio :deep(p) {
  margin-bottom: 1rem;
  line-height: 1.8;
}

.pastor-bio :deep(p:last-child) {
  margin-bottom: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-enter-to,
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.message-content :deep(p) {
  margin-bottom: 0.5rem;
  line-height: 1.7;
}

.message-content :deep(p:last-child) {
  margin-bottom: 0;
}
</style>
  