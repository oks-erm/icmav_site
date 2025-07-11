<template>
    <div>
      <!-- 1) FEATURED PASTORS (MAIN COUPLE) -->
      <div
        class="flex justify-center items-center py-4"
        data-aos="fade-up"
        data-aos-delay="100"
      >
        <div
          v-for="(p, i) in pastors.slice(0, 2)"
          :key="p.id"
          @click="toggleBio(p.id)"
          class="flex flex-col items-center cursor-pointer transition-transform hover:scale-102"
          :style="{ marginRight: i === 0 ? '-0.8rem' : '0' }"
        >
          <div class="w-38 h-38 rounded-full overflow-hidden shadow-lg">
            <img :src="p.photo" :alt="p.name" class="object-cover w-full h-full" />
          </div>
          <p class="mt-3 text-center font-medium whitespace-pre-line">{{ p.name }}</p>
        </div>
      </div>
  
      <!-- 1b) BIO FOR FEATURED COUPLE -->
      <transition name="slide-fade" mode="out-in">
        <div
          v-if="activePastor && activePastor.id <= 2"
          class="mb-8 px-10"
          data-aos="fade-up"
        >
          <div class="bg-base-100 rounded-lg shadow-lg p-6 text-base-content/90 leading-relaxed">
            <h3 class="text-2xl font-bold mb-4">{{ activePastor.name }}</h3>
            <img
              :src="activePastor.photo"
              :alt="activePastor.name"
              class="w-32 h-32 rounded-full object-cover float-left mr-4 mb-4 shadow-md"
            />
            <p class="whitespace-pre-line">{{ activePastor.bio }}</p>
          </div>
        </div>
      </transition>
  
      <!-- 2) WELCOME MESSAGE -->
      <div
        class="max-w-2xl mx-auto mb-2 px-6 py-8 bg-base-100 border border-gray-200 rounded-lg shadow-sm"
        data-aos="fade-up"
        data-aos-delay="200"
      >
        <p class="text-center text-gray-600">
          É com grande alegria que acolho você em nossa comunidade de fé, onde cada coração é valorizado e amado por Deus. Aqui caminhamos juntos, apoiando-nos mutuamente em oração, amor e serviço, para crescer cada vez mais na graça de Cristo. Que você se sinta em casa, encontrando neste lar espiritual um lugar de paz, esperança e renovação.
        </p>
      </div>
  
      <!-- 3) SCROLLABLE ROW OF THE REST -->
      <div class="relative">
        <div
          ref="scrollContainer"
          class="overflow-x-auto scroll-smooth hide-scrollbar py-6 px-8"
          @scroll="checkArrows"
        >
          <div
            class="flex"
            :class="isOverflowing ? 'justify-start' : 'justify-center'"
          >
            <div
              v-for="(p, i) in pastors.slice(2)"
              :key="p.id"
              @click="toggleBio(p.id)"
              class="flex-shrink-0 w-36 flex flex-col items-center cursor-pointer transition-transform hover:scale-103"
              :style="{
                marginRight:
                  (pastors.slice(2)[i + 1] &&
                    pastors.slice(2)[i + 1].spouseId === p.id)
                    ? '-0.8rem'
                    : '2.5rem'
              }"
              :data-aos="'fade-right'"
              :data-aos-delay="100 + i * 100"
            >
              <div class="w-36 h-36 rounded-full overflow-hidden shadow-lg">
                <img :src="p.photo" :alt="p.name" class="object-cover w-full h-full" />
              </div>
              <p class="mt-2 text-center font-medium whitespace-pre-line">{{ p.name }}</p>
            </div>
          </div>
        </div>
  
        <!-- Scroll Arrows -->
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
  
      <!-- 3b) BIO FOR REST OF PASTORS -->
      <transition name="slide-fade" mode="out-in">
        <div
          v-if="activePastor && activePastor.id > 2"
          class="px-10"
          data-aos="fade-up"
        >
          <div class="bg-base-100 rounded-lg shadow-lg p-6 text-base-content/90 leading-relaxed">
            <h3 class="text-2xl font-bold mb-4">{{ activePastor.name }}</h3>
            <img
              :src="activePastor.photo"
              :alt="activePastor.name"
              class="w-32 h-32 rounded-full object-cover float-left mr-4 mb-4 shadow-md"
            />
            <p class="whitespace-pre-line mb-6">{{ activePastor.bio }}</p>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  
  <script setup>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
  
  const pastors = [
    { id: 1, 
        name: 'Pr Henrique\nPereira', 
        photo: '/src/assets/h.png', 
        bio: '…', 
        spouseId: 2 },
    { id: 2, 
        name: 'Pra Minita\nPereira',  
        photo: '/src/assets/minita.png', 
        bio: '…', 
        spouseId: 1 },
    { id: 3, 
        name: 'Pr Rogério\nTrindade', 
        photo: '/src/assets/rog.png', 
        bio: 
        `   Rogério Trindade é casado com a Johana Antelo e têm dois filhos, o John e a Zoé. Nasceu na África do Sul, na cidade de Johanesburgo, fazendo parte de uma família de emigrantes portugueses e de cristãos comprometidos no serviço. 

        Foi pastor titular durante 3 anos de uma igreja evangélica local em Espanha, na cidade de Sevilha. É pastor auxiliar na ICMAV desde 2016. É Líder-coordenador da ICMAV com Propósitos e dos Ministérios de Ligação. É também Diretor e formador da ICMAV COLLEGE. Foi fundador da Escola de Liderança com Propósitos (LCP) em 2015, nome anterior da escola. É autor de mais de 30 manuais de treinamento para líderes.`, 
        spouseId: 4 },
    { id: 4, name: 'Pra Johana\nVillarroel', photo: '/src/assets/johana.png', bio: '…', spouseId: 3 },
    { id: 5, name: 'Pr Manza\nGarcia',     photo: '/src/assets/manza.png', bio: '…' },
    { id: 6, 
        name: 'Pr Paulo João\nCorreia',
        photo: '/src/assets/pj.png',    
        bio: 
        `   Paulo João é pastor de louvor e adoração na ICMAV, onde também lidera o ministério de homens. Casado com Denise, é pai de dois filhos e avô da Salomé. 
            
        A sua jornada no ministério começou aos 14 anos, após um encontro marcante com Jesus. Durante 18 anos serviu no Desafio Jovem, desenvolvendo trabalho evangelístico e social junto de comunidades vulneráveis e pessoas em situação de dependência.
            
        Desde 2006, dedica-se a tempo inteiro ao ministério pastoral, com ênfase no louvor, na formação de novas gerações e no discipulado de homens. A paternidade e a cultura do Reino no seio familiar são temas centrais da sua missão, procurando levantar líderes que vivam segundo o coração de Deus.`, spouseId: 7 },
    { id: 7, name: 'Pra Denise\nCorreia',  photo: '/src/assets/denise.png', bio: '…', spouseId: 6 },
    { id: 8, 
        name: 'Pr Danilo\nGujral',    
        photo: '/src/assets/danilo.png', 
        bio: 
        `   Nascido em Moçambique casado com Havani Gujral, pastor na ICMAV desde 2006 tendo já  ocupado várias areas de ministério na igreja. Atualmente eles são  responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até  ao Batismo nas Águas ou Membresia na Igreja. 

        Também supervisionam e treinam para o ministério  das várias equipas do Celebrando Restauração da ICMAV.  É produtor do programa  radiofónico "Ponto de Encontro" dirigido aos solteiros, divorciados e viúvos uma parceria com a Rádio Transmundial de Portugal.`, 
        spouseId: 9 },
    { id: 9, name: 'Pra Havani\nGujral',   
        photo: '/src/assets/havani.png', 
        bio:         
        `   Nascida no Brasil casada com Danilo Gujral, pastora na ICMAV desde 2006.

        Atualmente eles são  responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até  ao Batismo nas Águas ou Membresia na Igreja. Também supervisionam e treinam para o ministério  das várias equipas do Celebrando Restauração da ICMAV.`, 
        spouseId: 8 },

  ]

  // first two are featured
  const featuredPastors = pastors.slice(0,2)
  const otherPastors    = pastors.slice(2)
  
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

  /* bio transition */
  .slide-fade-enter-active,
  .slide-fade-leave-active {
    transition: all 0.2s ease;
  }

  /* slide-fade transition */
  .slide-fade-enter-active, .slide-fade-leave-active {
    transition: all 0.2s ease;
  }

  .slide-fade-enter-from, .slide-fade-leave-to {
    opacity: 0; transform: translateY(-10px);
  }

  .slide-fade-enter-to, .slide-fade-leave-from {
    opacity: 1; transform: translateY(0);
  }
  </style>
  