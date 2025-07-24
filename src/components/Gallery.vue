<!-- src/components/Gallery.vue -->
<template>
    <section id="gallery" class="py-1 sm:py-3 md:py-10 bg-gray-800">
      <div class="relative">
  
        <!-- Left Arrow -->
        <button
          @click="scrollPrev"
          class="absolute left-2 top-1/2 -translate-y-1/2 z-20 rounded-full p-2 transition"
          aria-label="Scroll previous"
        >
          <i class="fas fa-chevron-left text-xl text-gray-200"></i>
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
              class="object-cover w-full max-w-xs sm:max-w-sm md:w-144 md:h-96 md:max-w-lg"
            />
          </div>
        </div>
  
        <!-- Right Arrow -->
        <button
          @click="scrollNext"
          class="absolute right-2 top-1/2 -translate-y-1/2 z-20 rounded-full p-2 transition"
          aria-label="Scroll next"
        >
          <i class="fas fa-chevron-right text-xl text-gray-200"></i>
        </button>
  
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const pathBase = process.env.BASE_URL
  const images = [
    `${pathBase}photos/gallery/20250518_0033.jpg`,
    `${pathBase}photos/gallery/RVAZ0389.jpg`,
    `${pathBase}photos/gallery/RVAZ8702.jpg`,
    `${pathBase}photos/gallery/RVAZ8327.jpg`,
    `${pathBase}photos/gallery/20250323_0124.jpeg`,
    `${pathBase}photos/gallery/RVAZ8386.jpeg`,
    `${pathBase}photos/gallery/RVAZ8339.jpeg`,
    `${pathBase}photos/gallery/20250615_0043.jpeg`,
    `${pathBase}photos/gallery/20250518_0031.jpeg`,
    `${pathBase}photos/gallery/20250202_0230.jpeg`,
    `${pathBase}photos/gallery/20250629_0049.jpg`,
    `${pathBase}photos/gallery/20250629_0068.jpg`,
    `${pathBase}photos/gallery/RVAZ0610.jpg`,
    `${pathBase}photos/gallery/20250307_0710.jpg`
  ]

  const carousel = ref(null)
  
  // scroll by the width of one item (or adjust px as you like)
  const ITEM_WIDTH = 144 + 16 /* img width + space-x-4 */
  
  function scrollNext() {
  const el = carousel.value
  if (!el) return
  const atEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - 1
  if (atEnd) {
    // loop back to start
    el.scrollTo({ left: 0, behavior: 'auto' })
  } else {
    el.scrollBy({ left: ITEM_WIDTH, behavior: 'smooth' })
  }
}

    function scrollPrev() {
    const el = carousel.value
    if (!el) return
    const atStart = el.scrollLeft <= 1
    if (atStart) {
        // jump to very end
        const maxScroll = el.scrollWidth - el.clientWidth
        el.scrollTo({ left: maxScroll, behavior: 'smooth' })
    } else {
        el.scrollBy({ left: -ITEM_WIDTH, behavior: 'smooth' })
    }
    }
  </script>
  
  <style scoped>
  /* nothing extra needed here */
  </style>
  