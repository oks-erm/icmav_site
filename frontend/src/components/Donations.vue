<!-- src/components/Donations.vue -->

<template>
  <div class="mx-auto px-4 space-y-6">
    <div v-if="loading" class="text-center text-gray-500">
      A carregar conteúdo...
    </div>

    <div v-else-if="error" class="text-center text-red-600">
      {{ error }}
    </div>

    <div v-else class="text-center space-y-6">
      <div 
        class="max-w-6xl mx-auto text-center space-y-2" 
        v-html="donationsContent.donationsBody">
      </div>
      <blockquote class="max-w-3xl mx-auto text-center italic border-l-4 border-primary pl-4">
        “{{ donationsContent.donationsQuote }}”<br />
        <span class="font-medium">— {{ quoteReference }} —</span>
      </blockquote>
      <div class="pt-2 flex flex-col items-center gap-3">
        <RouterLink
          to="/donativos"
          class="inline-flex items-center justify-center rounded-full bg-primary px-8 py-4 text-base sm:text-lg font-bold text-white shadow-xl transition-all duration-300 hover:scale-[1.03] hover:bg-primary/90 cursor-pointer"
        >
          Fazer Contribuição
        </RouterLink>

        <!-- Indicador de Meios Aceites e Segurança -->
        <div class="flex items-center gap-3 text-xs text-gray-400 pt-1">
          <span class="flex items-center gap-1.5">
            <i class="fa-solid fa-lock text-emerald-400"></i>
            <span>Pagamento Seguro SSL</span>
          </span>
          <span>•</span>
          <span>MB WAY & SEPA</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getDonationsContent } from '../services/api'

const donationsContent = ref(null)
const loading = ref(true)
const error = ref('')

// The backend may store the reference under either field name:
//   • donationsQuoteReference — shipped in the default data
//   • donationsQuoteAuthor    — required by the validator on PUT
// Resolve whichever is present so the component always displays correctly.
const quoteReference = computed(() =>
  donationsContent.value?.donationsQuoteAuthor ??
  donationsContent.value?.donationsQuoteReference ??
  ''
)

onMounted(async () => {
  try {
    const data = await getDonationsContent()
    donationsContent.value = data.value || data
  } catch (err) {
    console.error('Failed to load donations content:', err)
    error.value = 'Erro ao carregar conteúdo.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
</style>