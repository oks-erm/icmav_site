<!-- src/components/CookieBanner.vue -->
<template>
  <transition name="cookie-slide">
    <aside
      v-if="showBanner"
      class="fixed bottom-3 inset-x-3 sm:bottom-4 sm:inset-x-4 max-w-3xl mx-auto z-[250] bg-gray-900/95 backdrop-blur-md text-gray-200 p-4 sm:p-5 rounded-2xl shadow-2xl border border-white/15"
      role="region"
      aria-label="Consentimento de Cookies"
    >
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <!-- Ícone e Mensagem -->
        <div class="flex items-start gap-3 flex-1">
          <div class="w-9 h-9 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0 mt-0.5 border border-amber-500/30">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 512 512" aria-hidden="true"><path d="M247.2 17c-22.1-3.1-44.6 .9-64.4 11.4l-74 39.5C89.1 78.4 73.2 94.9 63.4 115L26.7 190.6c-9.8 20.1-13 42.9-9.1 64.9l14.5 82.8c3.9 22.1 14.6 42.3 30.7 57.9l60.3 58.4c16.1 15.6 36.6 25.6 58.7 28.7l83 11.7c22.1 3.1 44.6-.9 64.4-11.4l74-39.5c19.7-10.5 35.6-27 45.4-47.2l36.7-75.5c9.8-20.1 13-42.9 9.1-64.9l-14.6-82.8c-3.9-22.1-14.6-42.3-30.7-57.9L388.9 57.5c-16.1-15.6-36.6-25.6-58.7-28.7L247.2 17zM208 144a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm-64 192a32 32 0 1 1 64 0 32 32 0 1 1 -64 0zm224-64a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>
          </div>
          <div class="text-xs sm:text-sm leading-relaxed text-gray-300">
            <p>
              Utilizamos cookies essenciais para garantir o funcionamento seguro e eficiente do nosso website. 
              Ao continuar a navegar, concorda com a nossa
              <router-link
                to="/politica-cookies"
                class="text-primary font-bold hover:underline"
              >
                Política de Cookies
              </router-link>.
            </p>
          </div>
        </div>

        <!-- Botões de Ação -->
        <div class="flex items-center gap-2 self-end sm:self-center flex-shrink-0 w-full sm:w-auto justify-end">
          <button
            type="button"
            @click="acceptEssential"
            class="px-3.5 py-2 rounded-xl text-xs font-semibold text-gray-300 bg-white/5 hover:bg-white/10 hover:text-white transition-all border border-white/10 cursor-pointer"
          >
            Apenas Essenciais
          </button>
          <button
            type="button"
            @click="acceptAll"
            class="px-4 py-2 rounded-xl text-xs font-bold text-white bg-primary hover:bg-primary/90 transition-all shadow-md cursor-pointer"
          >
            Aceitar Todos
          </button>
        </div>
      </div>
    </aside>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const COOKIE_STORAGE_KEY = 'icmav_cookie_consent'
const showBanner = ref(false)

onMounted(() => {
  try {
    const consent = localStorage.getItem(COOKIE_STORAGE_KEY)
    if (!consent) {
      // Pequeno atraso para entrada suave
      setTimeout(() => {
        showBanner.value = true
      }, 800)
    }
  } catch {
    // Caso localStorage esteja bloqueado pelo browser
    showBanner.value = false
  }
})

function acceptAll() {
  try {
    localStorage.setItem(COOKIE_STORAGE_KEY, 'all')
  } catch {}
  showBanner.value = false
}

function acceptEssential() {
  try {
    localStorage.setItem(COOKIE_STORAGE_KEY, 'essential')
  } catch {}
  showBanner.value = false
}
</script>

<style scoped>
.cookie-slide-enter-active,
.cookie-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.cookie-slide-enter-from,
.cookie-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
