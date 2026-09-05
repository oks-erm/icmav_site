<!-- src/views/MaintenanceView.vue -->

<template>
  <div class="min-h-screen flex flex-col bg-gray-900 text-white relative overflow-hidden">
    <!-- Background subtle glow -->
    <div class="absolute -top-40 -left-40 w-96 h-96 bg-primary/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-secondary/20 rounded-full blur-3xl pointer-events-none"></div>

    <div class="flex-grow flex flex-col items-center justify-center px-4 py-16 text-center z-10 max-w-2xl mx-auto">
      <!-- Logo -->
      <img
        src="/src/assets/logo_provisory_whitefull.png"
        alt="ICMAV - Igreja Cristã Manancial de Águas Vivas"
        class="h-16 md:h-20 w-auto mb-8 object-contain"
      />

      <!-- Tag -->
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-primary text-sm font-semibold mb-6 border border-white/10">
        <i class="fa-solid fa-wrench text-xs"></i>
        <span>Estamos em atualização</span>
      </div>

      <!-- Headline -->
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4 text-white">
        O nosso site está a ser renovado
      </h1>

      <p class="text-base sm:text-lg text-gray-300 mb-8 leading-relaxed">
        Estamos a preparar uma experiência ainda melhor para ti. Voltamos muito em breve! Enquanto isso, junta-te a nós presencialmente ou acompanha-nos nas redes sociais.
      </p>

      <!-- Sunday Service Box -->
      <div class="w-full bg-white/5 border border-white/10 rounded-2xl p-6 mb-8 text-left backdrop-blur-sm">
        <div class="flex items-start gap-4">
          <div class="w-10 h-10 rounded-xl bg-primary/20 text-primary flex items-center justify-center flex-shrink-0 text-lg">
            <i class="fa-solid fa-church"></i>
          </div>
          <div>
            <h3 class="font-bold text-white text-lg">Culto Dominical</h3>
            <p class="text-gray-300 text-sm mt-1">Todos os domingos às <strong>10h30</strong>.</p>
            <p class="text-gray-400 text-xs mt-1">Av. José Malhoa, Edifício Malhoa 27, Lisboa</p>
          </div>
        </div>
      </div>

      <!-- Social Links -->
      <div class="flex flex-col items-center gap-4">
        <p class="text-sm font-medium text-gray-400">Acompanha as nossas transmissões e novidades:</p>
        <div class="flex items-center gap-5 text-2xl text-gray-300">
          <a
            href="https://www.instagram.com/icmav_oficial/"
            target="_blank"
            rel="noopener noreferrer"
            class="hover:text-primary transition-colors"
            aria-label="Instagram da ICMAV"
          >
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a
            href="https://www.facebook.com/icmav"
            target="_blank"
            rel="noopener noreferrer"
            class="hover:text-primary transition-colors"
            aria-label="Facebook da ICMAV"
          >
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a
            href="https://www.youtube.com/@ICMAV"
            target="_blank"
            rel="noopener noreferrer"
            class="hover:text-primary transition-colors"
            aria-label="YouTube da ICMAV"
          >
            <i class="fa-brands fa-youtube"></i>
          </a>
        </div>
      </div>
    </div>

    <!-- Footer note -->
    <footer class="py-6 text-center text-xs text-gray-500 z-10 border-t border-white/5">
      &copy; {{ new Date().getFullYear() }} ICMAV — Todos os direitos reservados.
    </footer>
  </div>
</template>

<script setup>
</script>