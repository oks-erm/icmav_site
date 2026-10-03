<!-- src/components/Purpose.vue -->

<template>
  <section id="propositos" class="py-8 bg-base-100">
    <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
      <div class="flex flex-wrap -mx-4 justify-center">
        <div
          v-for="(p, i) in purposes"
          :key="p.title"
          class="s:w-full md:w-1/2 lg:w-1/3 px-4 mb-6 hover:scale-105 transition duration-300 ease-in-out"
        >
          <div
            class="flex items-start bg-white rounded-lg shadow-md transition h-full overflow-hidden"
            style="align-items: center;"
          >
            <div
              class="flex-shrink-0 w-20 h-full flex items-center justify-center text-2xl text-white"
              :class="p.bgClass"
            >
              <i :class="p.icon"></i>
            </div>

            <div class="ml-4 flex-1 flex flex-col p-4">
              <h3 class="text-lg font-bold mb-2">
                {{ p.title }}
              </h3>
              <p class="text-gray-600 flex-1">
                {{ p.desc }}
              </p>
              <p class="mt-4 italic text-sm text-gray-500">
                {{ p.biblicalPassage }} -
                <span class="font-medium">{{ p.biblicalReference }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPurposesContent } from '../services/api'

const purposes = ref([])

onMounted(async () => {
  try {
    const data = await getPurposesContent()
    if (Array.isArray(data.value)) {
      purposes.value = data.value
    }
  } catch (error) {
    console.error('Erro ao carregar purposes:', error)
  }
})
</script>

<style scoped>
</style>