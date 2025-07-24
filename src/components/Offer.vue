<template>
  <section class="pt-3 pb-2 md:pt-6 md:pb-6 bg-base-100">
    <div class="max-w-3xl mx-auto">

      <!-- Buttons (all on one line) -->
<!-- Buttons + inline boxes (mobile-first) -->
<div
  class="flex flex-col md:flex-row items-center md:items-start
         justify-center gap-6 px-6 md:px-10 lg:px-20"
  data-aos="fade-up"
  data-aos-delay="100"
>
  <!-- MB WAY -->
  <div class="flex flex-col items-center w-full md:w-auto">
    <button
      class="btn btn-success btn-lg rounded-full flex items-center space-x-3
             px-8 py-4 transition-transform hover:scale-105 w-full md:w-auto flex-nowrap whitespace-nowrap"
      @click="onMbWayClick"
    >
      <i class="fas fa-mobile-alt text-2xl"></i>
      <span class="text-lg font-semibold">MB WAY</span>
    </button>

    <transition name="fade-slide">
      <div
        v-if="showMbWay"
        id="mbway-box"
        class="bg-base-100 p-6 rounded-lg shadow-lg text-center mt-4
               w-full md:w-72"
        data-aos="fade-up"
        data-aos-delay="200"
      >
        <p class="text-lg font-semibold mb-2">MB WAY</p>
        <p class="text-xl font-bold">+351 934 693 310</p>
        <p class="text-sm text-gray-600 mt-2">
          (Use este número para pagamentos via MB WAY)
        </p>
      </div>
    </transition>
  </div>

  <!-- IBAN -->
  <div class="flex flex-col items-center w-full md:w-auto">
    <button
      class="btn btn-secondary btn-lg rounded-full flex items-center space-x-3
             px-8 py-4 transition-transform hover:scale-105 w-full md:w-auto flex-nowrap whitespace-nowrap"
      @click="toggleIban"
    >
      <i class="fas fa-university text-2xl"></i>
      <span class="text-lg font-semibold">Transferência (IBAN)</span>
    </button>

    <transition name="fade-slide">
      <div
        v-if="showIban"
        id="iban-box"
        class="bg-base-100 p-6 rounded-lg shadow-lg mt-4
               w-full md:w-80"
        data-aos="fade-up"
        data-aos-delay="200"
      >
        <div
          v-for="(item, idx) in bankDetails"
          :key="idx"
          class="flex justify-between items-center mb-2 last:mb-0"
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
    </transition>
  </div>

  <!-- PAYPAL (unchanged) -->
  <a
    href="https://paypal.me/icmav"
    target="_blank"
    class="btn btn-primary btn-lg rounded-full flex items-center space-x-3
           px-8 py-4 transition-transform hover:scale-105 w-full md:w-auto"
  >
    <i class="fab fa-paypal text-2xl"></i>
    <span class="text-lg font-semibold">PayPal</span>
  </a>
</div>


    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

// Toggle for showing/hiding the IBAN block
const showIban = ref(false)
// Toggle for showing/hiding the MB WAY block
const showMbWay = ref(false)

// Replace with your actual bank details:
const bankDetails = [
  { label: 'Banco', value: 'NOVO BANCO, SA' },
  { label: 'IBAN', value: 'PT50 0007 0246 0014 0750 0033 4' },
  { label: 'BIC/SWIFT', value: 'BESCPTPLXXX' },
  { label: 'Titular', value: 'Igreja ICMAV' },
]

// Keep track of which line was last copied (for tooltip text)
const copiedIndex = ref(null)

function toggleIban() {
  showIban.value = !showIban.value
  showMbWay.value = false // Hide MB WAY if IBAN is shown
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
  showMbWay.value = !showMbWay.value
  if (showMbWay.value) {
    showIban.value = false // Hide IBAN if MB WAY is shown
  }
}
</script>