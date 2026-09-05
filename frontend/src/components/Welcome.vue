<!-- src/components/Welcome.vue -->

<template>
  <section id="welcome-text" class="py-10 bg-gray-50">
    <p class="max-w-3xl mx-auto px-4 text-center text-lg text-base-content/80 space-y-4" v-html="infoContent" data-aos="fade-up"></p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWelcomeContent } from '../services/api'

const infoContent = ref('')

onMounted(async () => {
  try {
    const data = await getWelcomeContent()
    infoContent.value = data.value
  } catch (error) {
    infoContent.value = '<p>Não foi possível carregar este conteúdo neste momento.</p>'
  }
})
</script>

<style scoped>
</style>