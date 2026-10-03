<!-- src/components/ServicesBanner.vue -->

<template>
  <h2
    class="cursor-pointer text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center mb-1 py-4 px-4 md:px-0"
    @click="goToLocations"
    v-html="sanitizeHtml(servicesBannerContent)"
    data-aos="fade-up"
  >
  </h2>
</template>

<script setup>
import { sanitizeHtml } from '../utils/sanitize-html'
import { ref, onMounted } from 'vue'
import { getServicesBannerContent } from '../services/api'

const servicesBannerContent = ref('')

function goToLocations() {
  const section = document.getElementById('locations')
  if (section) {
    section.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

onMounted(async () => {
  try {
    const data = await getServicesBannerContent()
    servicesBannerContent.value = data.value
  } catch (error) {
    servicesBannerContent.value = '<p>Não foi possível carregar este conteúdo neste momento.</p>'
  }
})
</script>

<style scoped>
</style>
