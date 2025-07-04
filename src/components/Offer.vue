<template>
  <section class="py-6 bg-base-100">
    <div class="max-w-3xl mx-auto">

      <!-- Buttons (all on one line) -->
      <div
        class="flex justify-center gap-6 px-6 md:px-10 lg:px-20"
        data-aos="fade-up"
        data-aos-delay="100"
      >
        <!-- MB WAY Button -->
        <button
          class="btn btn-success btn-lg rounded-full flex items-center space-x-3 px-8 py-4 transition-transform hover:scale-105"
          @click="onMbWayClick"
        >
          <i class="fas fa-mobile-alt text-2xl"></i>
          <span class="text-lg font-semibold">MB WAY</span>
        </button>

        <!-- IBAN Toggle Button -->
        <button
          class="btn btn-secondary btn-lg rounded-full flex items-center space-x-3 px-8 py-4 transition-transform hover:scale-105"
          @click="toggleIban"
        >
          <i class="fas fa-university text-2xl"></i>
          <span class="text-lg font-semibold">Transferência (IBAN)</span>
        </button>

        <!-- PayPal Button -->
        <a
          href="https://paypal.me/icmav"
          target="_blank"
          class="btn btn-primary btn-lg rounded-full flex items-center space-x-3 px-8 py-4 transition-transform hover:scale-105"
        >
          <i class="fab fa-paypal text-2xl"></i>
          <span class="text-lg font-semibold">PayPal</span>
        </a>
      </div>

      <!-- IBAN DETAILS (visible only when showIban is true) -->
      <div v-if="showIban" class="mt-8 px-4 flex justify-center">
        <div
          id="iban-box"
          class="bg-base-100 p-6 rounded-lg shadow-lg space-y-4"
          data-aos="fade-up"
          data-aos-delay="200"
        >
          <!-- Loop through each bank detail line -->
          <div
            v-for="(item, idx) in bankDetails"
            :key="idx"
            class="flex justify-between items-center"
          >
            <span class="text-base">
              <strong>{{ item.label }}:</strong> {{ item.value }}
            </span>
            <button
              class="btn btn-ghost btn-xs tooltip tooltip-bottom"
              :data-tip="copiedIndex === idx ? 'Copiado!' : 'Copiar'"
              @click="copyToClipboard(item.value, idx)"
            >
              <i class="fas fa-copy text-lg"></i>
            </button>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

// Toggle for showing/hiding the IBAN block
const showIban = ref(false)

// Replace with your actual bank details:
const bankDetails = [
  { label: 'Banco', value: 'Caixa Geral de Depósitos' },
  { label: 'IBAN', value: 'PT50 0012 3456 7890 1234 5678 90' },
  { label: 'BIC/SWIFT', value: 'CGDIPTP1' },
  { label: 'Titular', value: 'Igreja ICMAV' },
]

// Keep track of which line was last copied (for tooltip text)
const copiedIndex = ref(null)

function toggleIban() {
  showIban.value = !showIban.value
}

function copyToClipboard(text, idx) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      copiedIndex.value = idx
      setTimeout(() => {
        if (copiedIndex.value === idx) {
          copiedIndex.value = null
        }
      }, 1500)
    })
    .catch((err) => {
      console.error('Erro ao copiar:', err)
    })
}

// Placeholder for MB WAY action
function onMbWayClick() {
  // e.g. scroll to a MB WAY section or open a modal
  console.log('MB WAY clicked')
}
</script>