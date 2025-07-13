<!-- src/components/Hero.vue -->
<template>
    <div class="relative w-full min-h-screen overflow-hidden">
        <!-- 1) Video background -->
        <video v-if="useVideo" class="absolute inset-0 w-full h-full object-cover" autoplay muted loop playsinline
            data-aos="fade-in">
            <source src="/src/assets/videos/hero.mp4" type="video/mp4" />
            <!-- Fallback if video fails -->
        </video>
        <img v-else src="/src/assets/fallbacks/hero.jpg" alt="Hero Background"
            class="absolute inset-0 w-full h-full object-cover" />

        <!-- 2) Dark overlay for better contrast -->
        <div class="absolute inset-0 bg-black/60"></div>

        <!-- 3) Centered headline + subline + words + circles + button -->
        <div class="relative z-10 flex flex-col items-center justify-center h-screen text-center px-4 space-y-6">
            <!-- Headline -->
            <h1 id="hero-text" class="text-5xl md:text-6xl font-extrabold text-white mb-4" data-aos="zoom-in">
                ICMAV - Propósito para a vida
            </h1>

            <!-- Sub-headline -->
            <!-- <p class="text-lg md:text-2xl text-white/90" data-aos="fade-up" data-aos-delay="200">
                Pertencer · Crescer · Servir · Alcançar · Adorar
            </p> -->

            <!-- Row of circles  -->
            <div
                class="flex flex-wrap justify-center space-x-8 mt-2"
                data-aos="fade-up"
                data-aos-delay="300"
            >
                <a
                v-for="(p, i) in propositos"
                :key="p.title"
                href="#propositos"
                class="w-14 h-14 rounded-full flex items-center justify-center text-2xl text-white shadow-lg m-0 transform transition-transform hover:scale-110"
                :class="`bg-${p.bg}`"
                data-aos="zoom-in"
                :data-aos-delay="300 + i * 150"
                >
                <i :class="`${p.icon} fa-fw`"></i>
                </a>
            </div>
            <button id="main-button" class="btn btn-outline btn-secondary rounded-full btn-wide btn-lg px-8" @click="scrollTo('info')">
                Começar
            </button>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Toggle to a static image if you prefer
const useVideo = ref(true)

function scrollTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

const propositos = [
    { title: 'Pertencer', icon: 'fas fa-users', bg: 'primary' },
    { title: 'Crescer', icon: 'fas fa-seedling', bg: 'secondary' },
    { title: 'Servir', icon: 'fas fa-hands-helping', bg: 'green-500' },
    { title: 'Alcançar', icon: 'fas fa-globe', bg: 'info' },
    { title: 'Adorar', icon: 'fas fa-sun', bg: 'yellow-300' },
]

onMounted(() => {
    // Re-initialize AOS after the video has started loading
    import('aos').then((AOS) => AOS.init({ duration: 800, once: true }))
})
</script>

<style scoped>
/* Ensure video never breaks its container */
video {
    object-fit: cover;
}
</style>
  
