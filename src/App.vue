<template>

  <Hero />

  <!-- Live Stream (Visible only when something is on) -->
  <!-- <section id="live" class="py-16 bg-gray-50">
    <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
      Transmissão ao Vivo
    </h2>
    <LiveStream />
  </section> -->


  <section id="app" class="py-16 bg-gray-50">
    <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
      Baixe o App
    </h2>
    <DownloadApp />
  </section>

  <!-- Ministérios -->
  <section id="ministerios" class="py-12 bg-base-100">
    <h2 class="text-3xl font-semibold text-center" data-aos="fade-up">
      Ministérios
    </h2>
    <MinistryCards />
  </section>

  <!-- Pastores -->
  <section id="pastores" class="py-16 bg-gray-50">
    <h2 class="text-3xl font-semibold text-center mb-10" data-aos="fade-up">
      Nossa Equipa Pastoral
    </h2>
    <Pastores />
  </section>

  <!-- Pequenos Grupos -->
  <section id="grupos" class="py-20">
    <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
      Pequenos Grupos
    </h2>
    <Groups />
  </section>

  <!-- Gallery -->
  <section id="gallery" class="py-10 bg-gray-800 text-base-100">
    <Gallery />
  </section>

  <!-- Social Media -->
  <section id="social" class="py-16 bg-primary text-base-100">
    <h2 class="text-3xl font-semibold text-center mb-1" data-aos="fade-up">
      Conecte-se Connosco
    </h2>
    <Social />
  </section>


  <!-- Oferta -->
  <section id="oferta" class="py-24 bg-base-100">
    <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
      Contribua
    </h2>
    <Offer />
  </section>

  <!-- Contact Section -->
  <section id="contactos" class="py-16 bg-gray-50">
    <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
      Contactos
    </h2>
    <Contact />
  </section>

  <Footer />
</template>

<script setup>
import { onMounted } from 'vue'
import AOS from 'aos'

import Gallery       from './components/Gallery.vue'
import Hero          from './components/Hero.vue'
import CircleGrid    from './components/CircleGrid.vue'
import MinistryCards from './components/MinistryCards.vue'
import Pastores      from './components/Pastores.vue'
import Groups        from './components/Groups.vue'
import Offer         from './components/Offer.vue'
import Social        from './components/Social.vue'
import LiveStream    from './components/LiveStream.vue'
import Contact       from './components/Contact.vue'
import DownloadApp   from './components/DownloadApp.vue'
import Footer        from './components/Footer.vue'

const propositos = [
  { title: 'Pertencer', icon: 'fas fa-users', bg: 'primary' },
  { title: 'Crescer', icon: 'fas fa-seedling', bg: 'secondary' },
  { title: 'Servir', icon: 'fas fa-hands-helping', bg: 'accent' },
  { title: 'Alcançar', icon: 'fas fa-globe', bg: 'info' },
  { title: 'Adorar', icon: 'fas fa-sun', bg: 'warning' },
]

const ministries = [
  { name: 'Adoração', icon: 'fas fa-music', link: 'https://icmav.org/adoracao' },
  { name: 'Jovens', icon: 'fas fa-users', link: 'https://icmav.org/jovens' },
  { name: 'Crianças', icon: 'fas fa-child', link: 'https://icmav.org/criancas' },
  { name: 'Mulheres', icon: 'fas fa-female', link: 'https://icmav.org/mulheres' },
  { name: 'Homens', icon: 'fas fa- hands - helping', link: 'https://icmav.org/homens' },
  { name: 'Alcançar', icon: 'fas fa-globe', link: 'https://icmav.org/alcançar' },
]

const social = [
  { icon: 'fab fa-facebook-f', link: 'https://facebook.com/icmav' },
  { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav' },
  { icon: 'fab fa-youtube', link: 'https://youtube.com/icmav' },
  { icon: 'fab fa-twitter', link: 'https://twitter.com/icmav' },
]


onMounted(() => {
  AOS.init({ duration: 800, once: true })
})
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
