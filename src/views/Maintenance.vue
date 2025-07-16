<!-- src/views/Maintenance.vue -->
<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-base-100 px-4">
    <!-- optional logo -->
    <img :src="logoSrc" alt="Logo" class="w-50 mb-8" />

    <!-- headline -->
    <h3 class="text-4xl font-bold mb-4 text-center">
      Site em manutenção
    </h3>

    <!-- sub-text
    <p class="text-lg text-center text-base-content/70 max-w-xl mb-8">
      Site em manutençao
    </p> -->

    <!-- call to action -->
  </div>
</template>

<script setup>
const base = process.env.BASE_URL
const logoSrc = `${base}logo_provisory.png`
</script>

<style scoped>
/* se quiser, troque o bg ou tipografia para combinar com seu tema */
</style>
