<!-- src/components/CircleGrid.vue -->
 
<template>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6 p-8">
        <div v-for="item in items" :key="item.title"
            class="card card-compact bg-base-100 shadow-lg hover:shadow-2xl transition" data-aos="fade-up">
            <div class="card-body items-center text-center">
                <div
                    :class="`bg-${item.bg} text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl mb-2`">
                    <i :class="item.icon"></i>
                </div>
                <h2 class="card-title">{{ item.title }}</h2>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    items: { type: Array, required: true }
})
</script>
  
<style scoped>
</style>