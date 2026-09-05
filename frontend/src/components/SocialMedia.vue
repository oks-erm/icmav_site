<template>
  <div class="bg-primary py-8">
    <div v-if="loading" class="text-center text-base-100" data-aos="fade-up">
      A carregar redes sociais...
    </div>

    <div v-else-if="error" class="text-center text-red-200" data-aos="fade-up">
      {{ error }}
    </div>

    <div v-else 
      class="flex justify-center gap-8" 
      data-aos="fade-up" 
      @mouseleave="hoveredSocial = null"
    >
      <a
        v-for="(s , i) in social"
        :key="i"
        @mouseenter="hoveredSocial = i"
        :href="s.link"
        target="_blank"
        rel="noopener noreferrer"
        class="social-icon w-12 h-12 flex items-center justify-center rounded-full bg-base-100 text-2xl text-primary transition-all duration-300 ease-out transform-gpu"
        :style="{ '--social-hover-color': s.hoverColor }"
        :class="getSocialScale(i)"
      >
        <i :class="`${s.icon} fa-fw`"></i>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSocialMediaContent } from '../services/api'

const social = ref([])
const loading = ref(true)
const error = ref('')
const hoveredSocial = ref(null)

async function loadSocialMedia() {
  loading.value = true
  error.value = ''

  try {
    const data = await getSocialMediaContent()
    social.value = Array.isArray(data.value) ? data.value : []
  } catch (err) {
    error.value = err.message || 'Erro ao carregar Redes Sociais'
    social.value = []
  } finally {
    loading.value = false
  }
}

function getSocialScale(i) {
    if (hoveredSocial.value === null) return 'scale-100'

    const distance = Math.abs(hoveredSocial.value - i)

    if (distance === 0) return 'scale-[1.25]'
    if (distance === 1) return 'scale-[1.00]'
    if (distance === 2) return 'scale-[1.00]'
    return 'scale-100'
}

onMounted(() => {
  loadSocialMedia()
})
</script>

<style scoped>
.social-icon {
  transition:
    transform 0.3s ease,
    background-color 0.25s ease,
    color 0.25s ease;
}

.social-icon:hover {
  background-color: var(--social-hover-color);
  color: white;
}
</style>