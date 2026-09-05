<!-- src/components/MinistriesPresentation.vue -->
 
<template>
    <section id="ministerios" class="py-12 bg-gray-100 ">
        <div class="max-w-7xl mx-auto px-4">
            <!-- FLEX WRAP CONTAINER -->
            <div class="flex flex-wrap -mx-4" data-aos="fade-up" data-aos-delay="200">
                <!-- EACH MINISTRY CARD -->
                <div 
                    v-for="(p, i) in ministries" 
                    :key="p.slug"
                    class="md:w-1/2 lg:w-1/3 px-4 mb-6"
                >
                    <router-link :to="{ name: 'MinistryDetail', params: { slug: p.slug } }"
                        class="flex items-start space-x-4 bg-base-100 rounded-lg shadow-lg hover:shadow-2xl hover:scale-105 transition p-6 h-full"
                        >
                        <!-- ICON CIRCLE -->
                        <div 
                            class="flex-shrink-0 w-14 h-14 flex items-center justify-center rounded-full text-3xl text-white"
                            :class="p.bgClass"
                        >
                            <i :class="p.icon"></i>
                        </div>

                        <!-- TITLE & DESCRIPTION -->
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-1">
                                {{ p.name }}
                            </h3>
                            <p class="text-sm text-base-content/70">
                                {{ p.desc }}
                            </p>
                        </div>
                    </router-link>
                </div>
                <!-- /END EACH CARD -->
            </div>
            <!-- /END FLEX WRAP CONTAINER -->
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getMinistriesPresentationContent } from '../services/api';

const ministries = ref([]);

onMounted(async () => {
  try {
    const data = await getMinistriesPresentationContent()
    if (Array.isArray(data.value)) {
      ministries.value = data.value
    }
  } catch (error) {
    console.error('Failed to load ministries:', error)
  } 
});
</script>
  
<style scoped>
</style>