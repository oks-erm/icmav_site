<!-- src/views/Home.vue -->

<template>
  <div class="min-h-screen">
    <!-- Hero section -->
    <Hero />

    <!-- Sticky header com menu à direita e logótipo à esquerda -->
    <StickyHeader />

    <!-- Who we are -->
    <section id="welcome" class="py-12 bg-gray-50 pb-6">
      <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-semibold text-center px-4 md:px-0" data-aos="fade-up">
        JUNTA-TE A NÓS
      </h1>
      <Welcome />
    </section>

    <!-- Services banner -->
    <section id="servicesBanner" class="py-6 bg-primary text-base-100">
      <ServicesBanner />
    </section>

    <!-- Our purposes -->
    <section id="purposes" class="py-12 bg-base-100 pb-4">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 pb-4" data-aos="fade-up">
        Os Nossos Propósitos
      </h2>
      <Purposes />
    </section>

    <!-- Pastoral team -->
    <section id="pastoralTeam" class="py-16 bg-gray-50">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 pb-4" data-aos="fade-up">
        Equipa Pastoral
      </h2>
      <PastoralTeam />
    </section>

    <!-- Ministries presentation -->
    <section id="ministriesPresentation" class="py-12 bg-gray-100 pb-4">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0" data-aos="fade-up">
        Conhece os nossos ministérios
      </h2>
      <MinistriesPresentation />
    </section>

    <!-- Local gatherings -->
    <section id="localGatherings" class="py-16 bg-gray-50">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 mb-8" data-aos="fade-up">
        Pequenos Grupos
      </h2>
      <LocalGatherings />
    </section>

    <!-- Gallery -->
    <section id="gallery" class="py-10 bg-gray-800 text-base-100">
      <Gallery />
    </section>

    <!-- Help request section -->
    <section id="helpRequest" class="py-16 bg-base-100">
      <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
        <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 mb-8">
          O que podemos fazer por ti?
        </h2>
        <HelpRequest />
      </div>
    </section>

    <!-- Social media -->
    <section id="socialMedia" class="py-16 bg-primary text-base-100">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 mb-1" data-aos="fade-up">
        Acompanha-nos online
      </h2>
      <SocialMedia />
    </section>

    <!-- Donations -->
    <section id="donations" class="py-16 bg-base-100">
      <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-semibold text-center px-4 md:px-0 mb-8" data-aos="fade-up">
        Contribui
      </h2>
      <Donations />
    </section>

    <!-- Locations -->
    <section id="locations" class="bg-gray-50">
      <Locations />
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import Hero                     from '../components/Hero.vue'
import StickyHeader             from '../components/StickyHeader.vue'
import Welcome                  from '../components/Welcome.vue'
import ServicesBanner           from '../components/ServicesBanner.vue'
import Purposes                 from '../components/Purposes.vue'
import PastoralTeam             from '../components/PastoralTeam.vue'
import MinistriesPresentation   from '../components/MinistriesPresentation.vue'
import LocalGatherings          from '../components/LocalGatherings.vue'
import Gallery                  from '../components/Gallery.vue'
import HelpRequest              from '../components/HelpRequest.vue'
import SocialMedia              from '../components/SocialMedia.vue'
import Donations                from '../components/Donations.vue'
import Locations                from '../components/Locations.vue'
import Footer                   from '../components/Footer.vue'

const route = useRoute()

function scrollToSection(hashWithPrefix) {
  if (!hashWithPrefix) return
  const id = hashWithPrefix.replace(/^#/, '')

  const scrollAttempt = () => {
    const el = document.getElementById(id)
    if (el) {
      const header = document.getElementById('site-sticky-header')
      const offset = header ? header.offsetHeight : 80
      const targetY = el.getBoundingClientRect().top + window.scrollY - offset
      window.scrollTo({
        top: Math.max(0, targetY),
        behavior: 'smooth',
      })
      return true
    }
    return false
  }

  nextTick(() => {
    // 1. Imediato
    scrollAttempt()
    // 2. Apaziguamento de renderização após montagem de dados e imagens assíncronas
    setTimeout(scrollAttempt, 150)
    setTimeout(scrollAttempt, 400)
    setTimeout(scrollAttempt, 800)
  })
}

onMounted(() => {
  if (route.hash) {
    scrollToSection(route.hash)
  }
})

watch(
  () => route.hash,
  (newHash) => {
    if (newHash) {
      scrollToSection(newHash)
    }
  }
)
</script>

<style scoped>
</style>