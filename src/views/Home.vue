<!-- src/views/Home.vue -->
<template>
    <Hero />
  
    <!-- Live Stream -->
    <section id="live" class="py-6 bg-primary text-base-100">
      <h2 class="text-3xl font-semibold text-center mb-1" data-aos="fade-up">
        Transmissão ao Vivo
      </h2>
      <LiveStream />
    </section>
  
    <!-- Quem Somos -->
    <section id="info" class="py-12 bg-gray-50 pb-6">
      <h2 class="text-3xl font-semibold text-center" data-aos="fade-up">
        Quem somos
      </h2>
      <Info />
    </section>
  
    <!-- Os Nossos Propósitos -->
    <section id="propositos" class="py-12 bg-base-100 pb-4">
      <h2 class="text-3xl font-semibold text-center" data-aos="fade-up">
        Os Nossos Propósitos
      </h2>
      <Propositos />
    </section>
  
    <!-- Equipa Pastoral -->
    <section id="pastores" class="py-16 bg-gray-50">
      <h2 class="text-3xl font-semibold text-center mb-10" data-aos="fade-up">
        Equipa Pastoral
      </h2>
      <Pastores />
    </section>

    <section id="reuniao" class="py-6 bg-primary text-base-100">
      <h2 class="text-3xl font-semibold text-center mb-1" data-aos="fade-up">
        Todos os domingos às 10h30 no ICMAV Polima.
      </h2>
    </section>
  
    <!-- Junta-te a nós -->
    <section id="ministerios" class="py-12 bg-base-100 pb-4">
      <h2 class="text-3xl font-semibold text-center" data-aos="fade-up">
        Junta-te a nós
      </h2>
      <MinistryCards />
    </section>
  
    <!-- Pequenos Grupos -->
    <section id="grupos" class="py-16 bg-gray-100">
      <h2 class="text-3xl font-semibold text-center mb-8" data-aos="fade-up">
        Pequenos Grupos
      </h2>
      <Groups />
    </section>
  
    <!-- Galeria -->
    <section id="gallery" class="py-10 bg-gray-800 text-base-100">
      <Gallery />
    </section>

    <section id="help" class="py-16 bg-base-100">
      <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
        <h2 class="text-3xl font-semibold text-center mb-8">
          O que podemos fazer por ti?
        </h2>
        <HelpSection />
      </div>
    </section>
  
    <!-- Conecte-se Connosco -->
    <section id="social" class="py-16 bg-primary text-base-100">
      <h2 class="text-3xl font-semibold text-center mb-1" data-aos="fade-up">
        Conecte-se Connosco
      </h2>
      <Social />
    </section>
  
    <!-- Oferta -->
    <section id="oferta" class="py-16 bg-base-100">
      <h2 class="text-3xl font-semibold text-center mb-6" data-aos="fade-up">
        Contribua
      </h2>
      <Offer />
    </section>
  
    <!-- Contactos -->
    <section id="contactos" class="py-16 bg-gray-50">
      <h2 class="text-3xl font-semibold text-center " data-aos="fade-up">
        Contactos & Extensões
      </h2>
      <Contact />
    </section>
  
    <Footer />
  </template>
  
  <script setup>
  import Hero          from '../components/Hero.vue'
  import LiveStream    from '../components/LiveStream.vue'
  import Info          from '../components/Info.vue'
  import Propositos    from '../components/Propositos.vue'
  import Pastores      from '../components/Pastores.vue'
  import MinistryCards from '../components/MinistryCards.vue'
  import Groups        from '../components/Groups.vue'
  import Gallery       from '../components/Gallery.vue'
  import Social        from '../components/Social.vue'
  import Offer         from '../components/Offer.vue'
  import Contact       from '../components/Contact.vue'
  import Footer        from '../components/Footer.vue'
  import HelpSection  from '../components/HelpSection.vue'
  </script>
  