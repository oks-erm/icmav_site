<!-- src/components/Hero.vue -->
<template>
    <div class="relative w-full min-h-screen overflow-hidden">
        <!-- Video background with device detection - always try video first -->
        <video 
            ref="heroVideo"
            class="absolute inset-0 w-full h-full object-cover" 
            autoplay 
            muted 
            loop 
            playsinline
            preload="auto"
            @loadeddata="handleVideoLoaded"
            @error="handleVideoError"
            data-aos="fade-in"
        >
            <source :src="getVideoSource()" type="video/mp4" />
            <!-- Fallback image only if browser doesn't support video -->
            <img :src="fallbackSrc" alt="Hero Background"
                class="absolute inset-0 w-full h-full object-cover" />
        </video>

        <!-- 2) Dark overlay for better contrast -->
        <div class="absolute inset-0 bg-black/40"></div>

        <!-- 3) Centered headline + subline + words + circles + button -->
        <div class="relative z-10 flex flex-col items-center justify-center h-screen text-center px-4 space-y-6">
            <!-- Headline -->
            <h1 id="hero-text" class="text-5xl md:text-6xl font-extrabold text-white mb-4" data-aos="zoom-in">
                <span id="hero-title">ICMAV</span>
                <!-- br shows on mobile, disappears ≥640 px -->
                <br class="sm:hidden" />
                <span class="hidden sm:inline">&nbsp;–&nbsp;&nbsp;</span>
                <span>Propósito para a vida</span>
            </h1>

            <!-- Sub-headline -->
            <!-- <p class="text-lg md:text-2xl text-white/90" data-aos="fade-up" data-aos-delay="200">
                Pertencer · Crescer · Servir · Alcançar · Adorar
            </p> -->

            <!-- Row of circles  -->
            <div
                class="flex flex-wrap justify-center space-x-4 md:space-x-8 mt-2"
                data-aos="fade-up"
                data-aos-delay="300"
            >
                <a
                v-for="(p, i) in propositos"
                :key="p.title"
                href="#propositos"
                class="w-12  h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center text-2xl text-white shadow-lg m-0 transform transition-transform hover:scale-110"
                :class="`bg-${p.bg}`"
                data-aos="zoom-in"
                :data-aos-delay="300 + i * 150"
                >
                <i :class="`${p.icon} fa-fw`"></i>
                </a>
            </div>
            <button id="main-button" class="btn btn-outline btn-secondary rounded-full btn-wide btn-lg px-8" @click="scrollTo('live')">
                Começar
            </button>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const base = process.env.BASE_URL
const fallbackSrc = `${base}fallbacks/hero.jpg`

const isVideoLoaded = ref(false)
const videoError = ref(false)
const heroVideo = ref(null)

// Device detection function
function getDeviceType() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera
    
    if (/android/i.test(userAgent) || /iPad|iPhone|iPod/.test(userAgent)) {
        return 'mobile'
    }
    
    if (/tablet|ipad/i.test(userAgent)) {
        return 'mobile'
    }
    
    return 'desktop'
}

// Get appropriate video source based on device
function getVideoSource() {
    const deviceType = getDeviceType()
    if (deviceType === 'mobile') {
        return `${base}videos/hero-mobile-480.mp4`
    } else {
        return `${base}videos/hero-desktop-1080.mp4`
    }
}

function handleVideoLoaded() {
    isVideoLoaded.value = true
    videoError.value = false
}

function handleVideoError() {
    console.log('Hero video failed to load, browser may not support video')
    videoError.value = true
}

// Smooth scroll to section
function scrollTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

const propositos = [
    { title: 'Pertencer', icon: 'fas fa-users', bg: 'primary' },
    { title: 'Crescer', icon: 'fas fa-seedling', bg: 'secondary' },
    { title: 'Servir', icon: 'fas fa-hands-helping', bg: 'success' },
    { title: 'Alcançar', icon: 'fas fa-globe', bg: 'info' },
    { title: 'Adorar', icon: 'fas fa-sun', bg: 'warning' },
]

onMounted(() => {
    import('aos').then((AOS) => AOS.init({ duration: 800, once: true }))
})
</script>

<style scoped>
video, img {
    object-fit: cover;
}

/* Optimize video performance on mobile */
@media (max-width: 768px) {
    video {
        transform: translateZ(0);
        -webkit-transform: translateZ(0);
    }
}
</style>

