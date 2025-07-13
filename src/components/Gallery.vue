<!-- src/components/Gallery.vue -->
<template>
    <section id="gallery" class="py-10 bg-gray-800">
      <div class="relative">
  
        <!-- Left Arrow -->
        <button
          @click="scrollPrev"
          class="absolute left-2 top-1/2 -translate-y-1/2 z-20 bg-white/80 rounded-full p-2 hover:bg-white transition"
          aria-label="Scroll previous"
        >
          <i class="fas fa-chevron-left text-xl text-gray-700"></i>
        </button>
  
        <!-- Carousel (overflow-x-auto) -->
        <div
          ref="carousel"
          class="carousel carousel-center w-full rounded-box overflow-x-auto scroll-smooth space-x-4 p-4"
          data-aos="fade-up"
          data-aos-delay="100"
        >
          <div
            v-for="(item, idx) in images"
            :key="idx"
            class="carousel-item flex-shrink-0 rounded-lg overflow-hidden"
          >
            <img
              :src="item"
              alt="Galeria Imagem"
              class="object-cover w-144 h-96"
            />
          </div>
        </div>
  
        <!-- Right Arrow -->
        <button
          @click="scrollNext"
          class="absolute right-2 top-1/2 -translate-y-1/2 z-20 bg-white/80 rounded-full p-2 hover:bg-white transition"
          aria-label="Scroll next"
        >
          <i class="fas fa-chevron-right text-xl text-gray-700"></i>
        </button>
  
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const images = [
    '/src/assets/photos/gallery/gallery2.png',
    '/src/assets/photos/gallery/gallery3.png',
    '/src/assets/photos/gallery/gallery4.png',
    '/src/assets/photos/gallery/gallery5.png',
    '/src/assets/photos/gallery/gallery3.png',
  ]
  
  const carousel = ref(null)
  
  // scroll by the width of one item (or adjust px as you like)
  const ITEM_WIDTH = 144 + 16 /* img width + space-x-4 */
  
  function scrollPrev() {
    if (!carousel.value) return
    carousel.value.scrollBy({ left: -ITEM_WIDTH, behavior: 'smooth' })
  }
  
  function scrollNext() {
    if (!carousel.value) return
    carousel.value.scrollBy({ left: +ITEM_WIDTH, behavior: 'smooth' })
  }
  </script>
  
  <style scoped>
  /* nothing extra needed here */
  </style>
  