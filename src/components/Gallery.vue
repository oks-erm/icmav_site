<!-- <template>
    <section id="gallery" class="py-16 bg-gray-800">
        <div class="carousel carousel-center bg-gray-800 w-full space-x-4 p-4" data-aos="fade-up" data-aos-delay="100">
            <div v-for="(img, i) in images" :key="i" class="carousel-item flex-shrink-0">
                <img :src="img" class="rounded-box object-cover h-96 w-144" alt="Galeria Imagem" />
            </div>
        </div>
    </section>
</template> -->
  
<template>
    <section id="gallery" class="py-10 bg-gray-800">
        <!-- Carousel wrapper -->
        <div class="carousel carousel-center w-full rounded-box overflow-x-auto space-x-4 p-4" data-aos="fade-up"
            data-aos-delay="100">
            <!-- Each carousel-item holds one image -->
            <div v-for="(item, idx) in images" :key="idx"
                class="carousel-item flex-shrink-0 rounded-lg overflow-hidden m-auto">
                <img :src="item" alt="Galeria Imagem" class="object-cover w-144 h-96" />
            </div>
        </div>
    </section>
</template>

<script setup>
const images = [
    '/src/assets/gallery2.png',
    '/src/assets/gallery3.png',
    '/src/assets/gallery4.png',
    '/src/assets/gallery5.png',
    '/src/assets/gallery3.png',
]
</script>
  
