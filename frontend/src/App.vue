<!-- src/App.vue -->
<template>
  <!-- this renders Home.vue at “/” or MinistryDetail.vue at “/ministerios/:slug” -->
  <router-view />
  <CookieBanner />
</template>

<script setup>
import CookieBanner from './components/CookieBanner.vue'
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
