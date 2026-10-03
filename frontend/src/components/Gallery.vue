<!-- src/components/Gallery.vue -->

<template>
  <section id="gallery" ref="gallerySection" class="py-10 bg-gray-800">
    <div class="overflow-hidden px-4">
      <div
        ref="track"
        class="flex gap-4 cursor-grab select-none touch-pan-y"
        :class="{ 'cursor-grabbing': isDragging }"
        :style="trackStyle"
        @mousedown="startDrag"
        @mousemove="onDrag"
        @mouseup="stopDrag"
        @mouseleave="stopDrag"
        @touchstart="startTouch"
        @touchmove="onTouchMove"
        @touchend="stopTouch"
        @touchcancel="stopTouch"
      >
        <div
          v-for="(item, idx) in renderedImages"
          :key="`${idx}-${item}`"
          class="flex-shrink-0 rounded-lg overflow-hidden"
        >
          <img
            :src="resolveImageUrl(item)"
            alt="Galeria de Fotografias ICMAV"
            loading="lazy"
            decoding="async"
            class="object-cover w-144 h-96 pointer-events-none"
            draggable="false"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { getGalleryContent } from '../services/api'

function resolveImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  if (url.startsWith('/uploads/')) return url
  if (url.startsWith('/src/assets/')) return url.replace('/src/assets/', '/')
  return url
}

const images = ref([])
const track = ref(null)
const gallerySection = ref(null)

const isDragging = ref(false)
const isAutoScrolling = ref(true)
const isVisible = ref(false)

const startX = ref(0)
const startY = ref(0)
const startOffset = ref(0)
const offsetX = ref(0)
const singleSetWidth = ref(0)

const touchDirectionLocked = ref(false)
const touchMode = ref(null) // 'horizontal' | 'vertical' | null

let animationFrameId = null
let lastTimestamp = null
let observer = null

const AUTO_SCROLL_SPEED = 45

const renderedImages = computed(() => {
  if (!images.value.length) return []
  return [...images.value, ...images.value]
})

const trackStyle = computed(() => ({
  transform: `translate3d(${-offsetX.value}px, 0, 0)`,
}))

async function loadGallery() {
  try {
    const data = await getGalleryContent()
    images.value = Array.isArray(data.value) ? data.value : []

    await nextTick()
    measureTrack()

    if (images.value.length > 1 && isVisible.value) {
      startAutoScroll()
    }
  } catch (error) {
    console.error('Erro ao carregar galeria:', error)
    images.value = []
  }
}

function measureTrack() {
  if (!track.value) return
  singleSetWidth.value = track.value.scrollWidth / 2
}

function normalizeOffset() {
  if (!singleSetWidth.value) return

  while (offsetX.value >= singleSetWidth.value) {
    offsetX.value -= singleSetWidth.value
  }

  while (offsetX.value < 0) {
    offsetX.value += singleSetWidth.value
  }
}

function autoScroll(timestamp) {
  if (lastTimestamp === null) {
    lastTimestamp = timestamp
  }

  const delta = (timestamp - lastTimestamp) / 1000
  lastTimestamp = timestamp

  if (isAutoScrolling.value && !isDragging.value && images.value.length > 1 && isVisible.value) {
    offsetX.value += AUTO_SCROLL_SPEED * delta
    normalizeOffset()
  }

  if (isVisible.value) {
    animationFrameId = requestAnimationFrame(autoScroll)
  }
}

function startAutoScroll() {
  stopAutoScroll()
  lastTimestamp = null
  if (isVisible.value && images.value.length > 1) {
    animationFrameId = requestAnimationFrame(autoScroll)
  }
}

function stopAutoScroll() {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }
  lastTimestamp = null
}

function startDrag(event) {
  isDragging.value = true
  isAutoScrolling.value = false
  startX.value = event.clientX
  startOffset.value = offsetX.value
}

function onDrag(event) {
  if (!isDragging.value) return

  event.preventDefault()
  const deltaX = event.clientX - startX.value
  offsetX.value = startOffset.value - deltaX
  normalizeOffset()
}

function stopDrag() {
  if (!isDragging.value) return

  isDragging.value = false
  isAutoScrolling.value = true
}

function startTouch(event) {
  const touch = event.touches[0]
  if (!touch) return

  startX.value = touch.clientX
  startY.value = touch.clientY
  startOffset.value = offsetX.value

  touchDirectionLocked.value = false
  touchMode.value = null
}

function onTouchMove(event) {
  const touch = event.touches[0]
  if (!touch) return

  const deltaX = touch.clientX - startX.value
  const deltaY = touch.clientY - startY.value

  if (!touchDirectionLocked.value) {
    if (Math.abs(deltaX) < 8 && Math.abs(deltaY) < 8) {
      return
    }

    touchDirectionLocked.value = true

    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      touchMode.value = 'horizontal'
      isDragging.value = true
      isAutoScrolling.value = false
    } else {
      touchMode.value = 'vertical'
      isDragging.value = false
      isAutoScrolling.value = true
      return
    }
  }

  if (touchMode.value !== 'horizontal') return

  event.preventDefault()
  offsetX.value = startOffset.value - deltaX
  normalizeOffset()
}

function stopTouch() {
  if (touchMode.value === 'horizontal') {
    isDragging.value = false
    isAutoScrolling.value = true
  }

  touchDirectionLocked.value = false
  touchMode.value = null
}

function handleResize() {
  measureTrack()
  normalizeOffset()
}

function handleVisibilityChange() {
  if (document.hidden) {
    stopAutoScroll()
  } else if (isVisible.value) {
    startAutoScroll()
  }
}

onMounted(async () => {
  // Intersection Observer para parar animação fora do ecrã
  if (typeof IntersectionObserver !== 'undefined' && gallerySection.value) {
    observer = new IntersectionObserver((entries) => {
      const entry = entries[0]
      isVisible.value = entry.isIntersecting
      if (isVisible.value) {
        startAutoScroll()
      } else {
        stopAutoScroll()
      }
    }, { threshold: 0.05 })

    observer.observe(gallerySection.value)
  } else {
    isVisible.value = true
  }

  await loadGallery()
  window.addEventListener('resize', handleResize)
  document.addEventListener('visibilitychange', handleVisibilityChange)
})

onBeforeUnmount(() => {
  stopAutoScroll()
  if (observer) {
    observer.disconnect()
    observer = null
  }
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})
</script>

<style scoped>
.touch-pan-y {
  touch-action: pan-y;
}
</style>