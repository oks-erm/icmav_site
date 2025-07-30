<template>
    <div class="bg-primary pt-8 pb-2 md:pb-8">
        <div class="flex justify-center space-x-6" data-aos="fade-up">
            <a v-for="(s, i) in social" :key="i" :href="s.link" target="_blank"
                class="social-icon w-12 h-12 flex items-center justify-center m-0 rounded-full color-base-200 text-2xl text-primary hover:bg-base-200 transition" >
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
    {
    icon: 'fab fa-whatsapp',
    link: 'https://chat.whatsapp.com/EdGaqNUARdYB7HokXeleHR'
  }
]
</script>

<style scoped>
.social-icon {
    background: #e0e5eb;
    color: #422ad5;
}

.social-icon:hover {
    background: #d1d9e0;
    color: #3a1fb8;
}
</style>
  
