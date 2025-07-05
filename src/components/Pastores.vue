<!-- src/components/Pastores.vue -->
<template>
    <div>
      <!-- 1) SCROLLABLE ROW OF PASTORES -->
      <div class="relative">
        <div
          ref="scrollContainer"
          class="overflow-x-auto scroll-smooth hide-scrollbar py-6 px-8"
          @scroll="checkArrows"
        >
          <div
            class="flex items-center"
            :class="isOverflowing ? 'justify-start' : 'justify-center'"
            style="align-items: baseline;"
          >
            <div
              v-for="(p,i) in pastors"
              :key="p.id"
              class="flex-shrink-0 w-36 flex flex-col items-center cursor-pointer transition-transform hover:scale-105"
              @click="toggleBio(p.id)"
              :style="{
                marginRight: (pastors[i+1] && pastors[i+1].id === p.spouseId)
                  ? '-0.8rem'
                  : '2.5rem'
              }"
              :data-aos="'fade-right'"
              :data-aos-delay="i * 100"
            >
              <div class="w-36 h-36 rounded-full overflow-hidden shadow-lg">
                <img :src="p.photo" :alt="p.name" class="object-cover w-full h-full" />
              </div>
              <p class="mt-2 text-center font-medium">{{ p.name }}</p>
            </div>
          </div>
        </div>
  
        <!-- scroll arrows -->
        <button
          v-if="showLeftArrow"
          class="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 hover:bg-white z-10"
          @click="scrollLeft"
        >
          <i class="fas fa-chevron-left text-xl text-gray-700"></i>
        </button>
        <button
          v-if="showRightArrow"
          class="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 hover:bg-white z-10"
          @click="scrollRight"
        >
          <i class="fas fa-chevron-right text-xl text-gray-700"></i>
        </button>
      </div>
  
      <!-- 2) DROP-DOWN BIO -->
      <transition name="slide-fade">
        <div v-if="activePastor" class="mt-8 px-4">
          <div class="bg-base-100 rounded-lg shadow-lg p-6 text-base-content/90 leading-relaxed" data-aos="fade-up">
            <h3 class="text-2xl px-36 font-bold mb-4">{{ activePastor.name }}</h3>
            <img
              :src="activePastor.photo"
              :alt="activePastor.name"
              class="w-32 h-32 rounded-full object-cover float-left mr-4 mb-4 shadow-md"
            />
            <p>{{ activePastor.bio }}</p>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
  
  const pastors = [
    { id: 1, name: 'Pr Henrique Pereira', photo: '/src/assets/h.png', bio: '…', spouseId: 2 },
    { id: 2, name: 'Pra Minita Pereira',  photo: '/src/assets/minita.png', bio: '…', spouseId: 1 },
    { id: 3, name: 'Pr Rogério Trindade', photo: '/src/assets/rog.png', bio: '…', spouseId: 4 },
    { id: 4, name: 'Pra Johana Villarroel', photo: '/src/assets/johana.png', bio: '…', spouseId: 3 },
    { id: 5, name: 'Pr Manza Garcia',     photo: '/src/assets/manza.png', bio: '…' },
    { id: 6, name: 'Pr Danilo Gujral',    photo: '/src/assets/danilo.png', bio: '…', spouseId: 7 },
    { id: 7, name: 'Pra Havani Gujral',   photo: '/src/assets/havani.png', bio: '…', spouseId: 6 },
    { id: 8, name: 'Pr Paulo João Correia',photo: '/src/assets/pj.png',    bio: '…', spouseId: 9 },
    { id: 9, name: 'Pra Denise Correia',  photo: '/src/assets/denise.png', bio: '…', spouseId: 8 },
  ]
  
  // dropdown state
  const activeId = ref(null)
  function toggleBio(id) {
    activeId.value = activeId.value === id ? null : id
  }
  const activePastor = computed(() => pastors.find(p => p.id === activeId.value))
  
  // scrolling & arrows
  const scrollContainer = ref(null)
  const showLeftArrow  = ref(false)
  const showRightArrow = ref(false)
  const isOverflowing  = ref(false)
  
  function checkArrows() {
    const el = scrollContainer.value
    if (!el) return
    showLeftArrow.value  = el.scrollLeft > 10
    showRightArrow.value = el.scrollLeft + el.clientWidth + 10 < el.scrollWidth
    isOverflowing.value  = el.scrollWidth > el.clientWidth
  }
  
  function scrollLeft() {
    scrollContainer.value?.scrollBy({ left: -200, behavior: 'smooth' })
  }
  function scrollRight() {
    scrollContainer.value?.scrollBy({ left: +200, behavior: 'smooth' })
  }
  
  onMounted(() => {
    checkArrows()
    window.addEventListener('resize', checkArrows)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('resize', checkArrows)
  })
  </script>
  
  <style scoped>
  .hide-scrollbar {
    scrollbar-width: none;
  }
  .hide-scrollbar::-webkit-scrollbar {
    display: none;
  }
  
  /* slide-fade transition */
  .slide-fade-enter-active, .slide-fade-leave-active {
    transition: all 0.3s ease;
  }
  .slide-fade-enter-from, .slide-fade-leave-to {
    opacity: 0; transform: translateY(-10px);
  }
  .slide-fade-enter-to, .slide-fade-leave-from {
    opacity: 1; transform: translateY(0);
  }
  </style>
  