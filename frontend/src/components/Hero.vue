<!-- src/components/Hero.vue -->

<template>
    <div class="relative w-full min-h-screen overflow-hidden">
        <video
            v-if="useVideo"
            class="absolute inset-0 w-full h-full object-cover"
            autoplay
            muted
            loop
            playsinline
            preload="metadata"
            data-aos="fade-in"
        >
            <source src="/src/assets/videos/hero.mp4" type="video/mp4" />
        </video>

        <img
            v-else
            src="/src/assets/fallbacks/hero.jpg"
            alt="Hero Background ICMAV"
            fetchpriority="high"
            decoding="async"
            class="absolute inset-0 w-full h-full object-cover"
        />

        <div class="absolute inset-0 bg-black/40"></div>

        <div class="relative z-10 flex flex-col items-center justify-center h-screen text-center px-4 gap-8 md:gap-14">
            <div class="flex flex-col items-center space-y-4">
                <img
                    src="/src/assets/logo_provisory_white.png"
                    alt="Logo ICMAV"
                    fetchpriority="high"
                    decoding="async"
                    class="w-[28%] md:w-[20%]"
                    data-aos="zoom-in"
                />
                <img
                    src="/src/assets/logo_provisory_whitenaming.png"
                    alt="Nome Igreja ICMAV"
                    fetchpriority="high"
                    decoding="async"
                    class="w-[65%] md:w-[40%]"
                    data-aos="zoom-in"
                />
            </div>

            <p class="text-xl md:text-3xl text-white/90" data-aos="fade-up" data-aos-delay="200">
                Propósito para a vida
            </p>

            <div class="flex flex-col items-center space-y-4">
                <!-- Ícones dos propósitos só visíveis quando cabem todos numa só linha (>= md) -->
                <div
                    class="hidden md:flex flex-wrap justify-between gap-16"
                    data-aos="fade-up"
                    data-aos-delay="300"
                    @mouseleave="hoveredPurpose = null"
                >
                    <a
                        v-for="(p, i) in purposes"
                        :key="p.title"
                        @click="scrollTo('purposes')"
                        @mouseenter="hoveredPurpose = i"
                        class="flex flex-col items-center gap-2 text-white cursor-pointer origin-bottom transform-gpu transition-all duration-300 ease-out"
                        :class="getDockScale(i)"
                    >
                        <div
                            :class="[
                                'w-14 h-14 rounded-full flex items-center justify-center text-xl shadow-lg transition-all duration-300 ease-out',
                                p.bgClass
                            ]"
                        >
                            <i :class="`${p.icon} fa-fw`"></i>
                        </div>

                        <span class="text-sm md:text-base font-medium transition-all duration-300 ease-out">
                            {{ p.title }}
                        </span>
                    </a>
                </div>

                <button
                    id="main-button"
                    class="btn btn-outline btn-secondary rounded-full btn-wide btn-lg px-8 -mt-4 cursor-pointer"
                    @click="scrollTo('welcome')"
                >
                    Vem conhecer-nos
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPurposesContent } from '../services/api'

const useVideo = ref(true)
const purposes = ref([])
const hoveredPurpose = ref(null)

function scrollTo(id) {
    const el = document.getElementById(id)
    const header = document.getElementById('site-sticky-header')
    if (!el) return

    const headerOffset = header ? header.offsetHeight : 72
    const elementPosition = el.getBoundingClientRect().top + window.scrollY
    const offsetPosition = elementPosition - headerOffset

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    })
}

function getDockScale(i) {
    if (hoveredPurpose.value === null) return 'scale-100'

    const distance = Math.abs(hoveredPurpose.value - i)

    if (distance === 0) return 'scale-[1.40]'
    if (distance === 1) return 'scale-[1.15]'
    if (distance === 2) return 'scale-[1.05]'
    return 'scale-100'
}

onMounted(async () => {
  try {
    const data = await getPurposesContent()
    if (Array.isArray(data.value)) {
      purposes.value = data.value
    }
  } catch (error) {
    console.error('Erro ao carregar purposes:', error)
  }
})
</script>

<style scoped>
video {
    object-fit: cover;
}
</style>