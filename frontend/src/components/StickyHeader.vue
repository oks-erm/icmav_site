<!-- src/components/StickyHeader.vue -->

<template>
  <header
    id="site-sticky-header"
    class="sticky top-0 z-[100] bg-gray-900 shadow-md border-b border-white/10 w-full"
  >
    <div class="w-full px-6 sm:px-8 lg:px-10">
      <div class="flex items-center justify-between h-20 gap-4">
        <!-- Canto Esquerdo: Ícone / Logótipo da ICMAV -->
        <button
          type="button"
          @click="handleLogoClick"
          class="flex items-center cursor-pointer focus:outline-none flex-shrink-0"
          aria-label="ICMAV - Voltar ao topo"
        >
          <img :src="logo" alt="ICMAV" class="h-10 md:h-12 w-auto object-contain" />
        </button>

        <!-- Menu Desktop: Encostado à direita com os 8 atalhos ordenados -->
        <nav class="hidden lg:flex items-center justify-end gap-5 xl:gap-7 text-sm font-medium text-gray-300">
          <a
            v-for="item in navLinks"
            :key="item.name"
            @click.prevent="navigateTo(item.hash)"
            class="hover:text-white transition-colors cursor-pointer whitespace-nowrap py-1 px-1 hover:text-primary"
          >
            {{ item.name }}
          </a>
        </nav>

        <!-- Botão Hambúrguer para Mobile/Tablet (< lg) -->
        <button
          type="button"
          class="lg:hidden flex items-center justify-center w-10 h-10 rounded-xl text-gray-200 hover:text-white hover:bg-white/10 transition-colors focus:outline-none cursor-pointer"
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          :aria-label="isMobileMenuOpen ? 'Fechar menu' : 'Abrir menu de navegação'"
        >
          <i :class="isMobileMenuOpen ? 'fa-solid fa-xmark text-xl' : 'fa-solid fa-bars text-xl'"></i>
        </button>
      </div>
    </div>

    <!-- ══════════════════ MOBILE DRAWER (LG:HIDDEN) ══════════════════ -->
    <teleport to="body">
      <!-- Backdrop móvel -->
      <transition name="fade">
        <div
          v-if="isMobileMenuOpen"
          class="lg:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-[200]"
          @click="isMobileMenuOpen = false"
        ></div>
      </transition>

      <!-- Drawer deslizante para Mobile -->
      <transition name="slide-left">
        <aside
          v-if="isMobileMenuOpen"
          class="lg:hidden fixed top-0 left-0 bottom-0 w-80 max-w-[85vw] bg-gray-900 text-white z-[201] shadow-2xl border-r border-white/10 flex flex-col justify-between"
          role="dialog"
          aria-modal="true"
          aria-label="Menu Móvel"
        >
          <!-- Topo do Drawer móvel -->
          <div class="h-20 px-6 border-b border-white/10 flex items-center justify-between">
            <img :src="logo" alt="ICMAV" class="h-10 w-auto object-contain" />
            <button
              type="button"
              class="w-10 h-10 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 flex items-center justify-center transition-colors cursor-pointer"
              @click="isMobileMenuOpen = false"
              aria-label="Fechar menu"
            >
              <i class="fa-solid fa-xmark text-xl"></i>
            </button>
          </div>

          <!-- Links do Drawer móvel ordenados -->
          <nav class="flex-grow p-6 overflow-y-auto space-y-2">
            <a
              v-for="item in navLinks"
              :key="item.name"
              @click.prevent="navigateTo(item.hash); isMobileMenuOpen = false"
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-medium text-gray-200 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
            >
              <i :class="[item.icon, 'w-5 text-center text-primary/80']"></i>
              <span>{{ item.name }}</span>
            </a>
          </nav>
        </aside>
      </transition>
    </teleport>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import logo from '../assets/logo_provisory_whitefull.png'

const route = useRoute()
const router = useRouter()

const isMobileMenuOpen = ref(false)

// Lista restrita aos 8 itens solicitados na ordem exata
const navLinks = [
  { name: 'Propósitos', hash: 'purposes', icon: 'fa-solid fa-compass' },
  { name: 'Equipa', hash: 'pastoralTeam', icon: 'fa-solid fa-users' },
  { name: 'Ministérios', hash: 'ministriesPresentation', icon: 'fa-solid fa-hand-holding-heart' },
  { name: 'Pequenos Grupos', hash: 'localGatherings', icon: 'fa-solid fa-house-chimney-user' },
  { name: 'Cuidado', hash: 'helpRequest', icon: 'fa-solid fa-hands-holding' },
  { name: 'Redes Sociais', hash: 'socialMedia', icon: 'fa-solid fa-share-nodes' },
  { name: 'Contribuir', hash: 'donations', icon: 'fa-solid fa-hand-holding-dollar' },
  { name: 'Localizações', hash: 'locations', icon: 'fa-solid fa-location-dot' },
]

function navigateTo(hash) {
  isMobileMenuOpen.value = false

  const cleanHash = hash.replace(/^#/, '')
  const isHomePage = route.name === 'Home' || route.name === 'Root' || route.path === '/'

  if (!isHomePage) {
    router.push({ path: '/', hash: `#${cleanHash}` })
    return
  }

  const el = document.getElementById(cleanHash)
  if (el) {
    const header = document.getElementById('site-sticky-header')
    const offset = header ? header.offsetHeight : 80
    const elementPosition = el.getBoundingClientRect().top + window.scrollY
    window.scrollTo({
      top: Math.max(0, elementPosition - offset),
      behavior: 'smooth',
    })
    window.history.replaceState(null, '', `#${cleanHash}`)
  } else {
    router.push({ hash: `#${cleanHash}` })
  }
}

function handleLogoClick() {
  isMobileMenuOpen.value = false
  if (route.name !== 'Home' && route.name !== 'Root') {
    router.push({ name: 'Home' })
    return
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleKeydown(e) {
  if (e.key === 'Escape' && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Mobile Drawer Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-left-enter-from,
.slide-left-leave-to {
  transform: translateX(-100%);
}
</style>