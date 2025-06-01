<template>
    <div class="bg-primary py-8">
        <div class="flex justify-center space-x-6" data-aos="fade-up">
            <a v-for="(s, i) in social" :key="i" :href="s.link" target="_blank"
                class="w-12 h-12 flex items-center justify-center m-0 rounded-full bg-base-100 text-2xl text-primary hover:bg-base-200 transition">
                <i :class="`${s.icon} fa-fw`"></i>
            </a>
        </div>
    </div>
</template>

<script setup>
const social = [
    { icon: 'fab fa-facebook-f', link: 'https://facebook.com/icmav' },
    { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav' },
    { icon: 'fab fa-youtube', link: 'https://www.youtube.com/@igrejaICMAV' },
    { icon: 'fab fa-tiktok', link: 'https://tiktok.com/icmav' },
]
</script>

<style scoped>
</style>
  
