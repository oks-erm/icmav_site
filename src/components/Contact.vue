<!-- src/components/ContactExtensions.vue -->
<template>
  <div class="max-w-4xl mx-auto py-8 px-4" data-aos="fade-up">
    <div class="flex flex-col md:flex-row items-center">
      <!-- Vertical Tabs -->
      <div class="tabs tabs-vertical flex-shrink-0 mb-6 space-y-2">
        <a
          v-for="(ext, i) in extensions"
          :key="ext.slug"
          @click="selectedIndex = i"
          :class="[
            'btn',
            'cursor-pointer',
            'min-w-[8rem]',
            'rounded-full',
            'flex',
            'items-center',
            'justify-center',
            'text-lg',
            'font-semibold',
            'py-2',
            'px-6',
            'transition-colors',
            'duration-200',
            'ease-in-out',
            selectedIndex === i
              ? 'btn-primary'
              : 'btn-primary btn-outline'
          ]"
        >
          {{ ext.name }}
        </a>
      </div>
      <!-- Tab Content (centered text) -->
      <div class="flex-1 md:pl-8 space-y-0.5 text-lg text-center">
        <p>
          <i class="fas fa-envelope"></i>
          Email:
          <a :href="`mailto:${current.email}`" class="text-primary underline">
            {{ current.email }}
          </a>
        </p>
        <p>
          <i class="fas fa-phone"></i>
          Telefone:
          <a :href="`tel:${current.phone}`" class="text-primary underline">
            {{ current.phone }}
          </a>
        </p>
        <p>
          <i class="fas fa-map-marker-alt"></i>
          Endereço: {{ current.address }}
        </p>
        <p v-if="current.website">
          <i class="fas fa-globe"></i>
          Site:
          <a
            :href="current.website"
            target="_blank"
            rel="noopener"
            class="text-primary underline"
          >
            {{ current.website }}
          </a>
        </p>

        <!-- Map Embed -->
        <div class="h-64 w-full rounded-lg overflow-hidden shadow-lg">
          <iframe
            :src="current.mapEmbedUrl"
            class="w-full h-full"
            style="border:0;"
            allowfullscreen
            loading="lazy"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const extensions = [
  {
    slug: 'sede',
    name: 'Polima',
    email: 'ccicmav@gmail.com',
    phone: '+351 934 693 310',
    address: 'Estrada de Polima 609, 2785-303 São Domingos de Rana',
    mapEmbedUrl:
      'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d927.0658016320806!2d-9.328997091208173!3d38.72404304543485!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd1ecf1ea14b0a83%3A0x142331a801f14075!2sIgreja%20Evang%C3%A9lica%20Crist%C3%A3%20ICMAV!5e0!3m2!1spt-PT!2spt!4v1748728354732!5m2!1spt-PT!2spt',
    website: 'https://icmav.pt'
  },
  {
    slug: 'caparica',
    name: 'Caparica',
    email: 'caparica@icmav.org',
    phone: '+351 212 345 678',
    address: 'Av. da Caparica 123, 2825-123 Caparica',
    mapEmbedUrl:
      'https://www.google.com/maps/embed?pb=!1m18!...caparica...',
    website: null
  },
  {
    slug: 'setubal',
    name: 'Setúbal',
    email: 'setubal@icmav.org',
    phone: '+351 265 123 456',
    address: 'Rua de Setúbal 45, 2900-456 Setúbal',
    mapEmbedUrl:
      'https://www.google.com/maps/embed?pb=!1m18!...setubal...',
    website: null
  },
  {
    slug: 'londres',
    name: 'Londres',
    email: 'church@icmavlondon.com',
    phone: '+44 47940509951',
    address: '125, Gibraltar Crescent, Epsom, KT19 9BU, Londres, UK',
    mapEmbedUrl:
      "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2492.053264944142!2d-0.2617746874167882!3d51.34693115432881!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x487609e1e2c18b91%3A0x53b7320aedd8485c!2s125%20Gibraltar%20Cres%2C%20Epsom%20KT19%209BU%2C%20UK!5e0!3m2!1sen!2spt!4v1751627209795!5m2!1sen!2spt",
    website: 'https://icmavlondon.com/'
  }
]

const selectedIndex = ref(0)
const current = computed(() => extensions[selectedIndex.value])
</script>

<style scoped>
/* no extra CSS needed—DaisyUI and Tailwind handle the centering */
</style>
