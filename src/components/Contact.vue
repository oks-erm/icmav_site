<!-- src/components/ContactExtensions.vue -->
<template>
    <div class="max-w-4xl mx-auto py-8 px-4" data-aos="fade-up">
    <div class="flex !flex-col items-center">
      <!-- 🍋 Button “tabs” -->
      <div class="flex flex-col md:flex-row mb-6">
        <button
          v-for="(ext, i) in extensions"
          :key="ext.slug"
          @click="selectedIndex = i"
          class="btn w-40 normal-case text-lg font-semibold rounded-full transition-colors mx-1 duration-200 mb-1 md:mb-0"
          :class=" selectedIndex === i 
            ? 'btn-primary' 
            : 'btn-outline btn-primary hover:btn-secondary' 
          "
        >
          {{ ext.name }}
        </button>
      </div>
      <!-- Tab Content (centered text) -->
      <div class="flex-1 md:pl-8 space-y-0.5 text-lg text-center">
        <div class="mb-6">
        <p>
          <i class="fas fa-calendar-alt"></i>
          Culto de Domingo: {{ current.sundayService }}
        </p>
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
    </div>

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
    website: 'icmav.pt',
    sundayService: '10h30'
  },
  {
    slug: 'caparica',
    name: 'Caparica',
    email: 'icmavmontedecaparica@gmail.com',
    phone: '+351 934 693 310',
    address: 'Rua de Bela Vista nº 110 R/C-A. 2825-165 Caparica',
    mapEmbedUrl:
      'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3115.198258037662!2d-9.194091488196118!3d38.667311471656376!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd1ecad566b62271%3A0xeda658899ac7783!2sR.%20da%20Bela%20Vista%20110%2C%202825-165%20Caparica!5e0!3m2!1sen!2spt!4v1751717000927!5m2!1sen!2spt',
    website: null,
    sundayService: '10h30'
  },
  {
    slug: 'setubal',
    name: 'Setúbal',
    email: 'ccicmav@gmail.com',
    phone: '+351 934 069 320',
    address: 'R. Abel Salazar 14, 2910-372 Setúbal',
    mapEmbedUrl:
      "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3121.2323521355816!2d-8.8771158!3d38.52841179999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd19439761d6bb03%3A0x7c9346ba04ce5508!2sIgreja%20evang%C3%A9lica%20ICMAV%20-%20Set%C3%BAbal!5e0!3m2!1sen!2spt!4v1751717171155!5m2!1sen!2spt",
    website: null,
    sundayService: '10h30'
  },
  {
    slug: 'londres',
    name: 'Londres',
    email: 'church@icmavlondon.com',
    phone: '+44 47940509951',
    address: '125, Gibraltar Crescent, Epsom, KT19 9BU, Londres, UK',
    mapEmbedUrl:
      "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2492.053264944142!2d-0.2617746874167882!3d51.34693115432881!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x487609e1e2c18b91%3A0x53b7320aedd8485c!2s125%20Gibraltar%20Cres%2C%20Epsom%20KT19%209BU%2C%20UK!5e0!3m2!1sen!2spt!4v1751627209795!5m2!1sen!2spt",
    website: 'icmavlondon.com',
    sundayService: '10h30'
  }
]

const selectedIndex = ref(0)
const current = computed(() => extensions[selectedIndex.value])
</script>

<style scoped>
/* no extra CSS needed—DaisyUI and Tailwind handle the centering */
</style>
