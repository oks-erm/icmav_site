<!-- src/views/NotFoundView.vue -->

<template>
  <div class="min-h-screen flex flex-col bg-gray-900 text-white">
    <StickyHeader />

    <main class="flex-grow flex items-center justify-center px-4 py-16 text-center">
      <div class="max-w-md space-y-6">
        <div class="text-primary text-7xl font-extrabold tracking-widest">
          404
        </div>

        <h1 class="text-3xl font-bold tracking-tight sm:text-4xl text-white">
          Página não encontrada
        </h1>

        <p class="text-gray-400 text-base">
          O endereço que procuras não existe ou foi alterado. Regressa à página principal para continuar a navegar no site da ICMAV.
        </p>

        <div class="pt-4">
          <router-link
            to="/"
            class="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-primary text-white font-semibold shadow-lg hover:bg-primary/90 transition-all hover:scale-105 active:scale-95 cursor-pointer"
          >
            <i class="fa-solid fa-house"></i>
            <span>Ir para o Início</span>
          </router-link>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import StickyHeader from '../components/StickyHeader.vue'
import Footer from '../components/Footer.vue'
</script>
