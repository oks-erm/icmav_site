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
            O nosso  desejo é que cada pessoa que chegue até nós se sinta em casa, seja inspirada pela Palavra de Deus e encontre o apoio necessário para viver uma vida plena e com muito significado. És muito bem vindo à nossa comunidade queremos muito conhecer-te e partilhar contigo a alegria de caminhar na fé juntos!
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

  const pathBase = process.env.BASE_URL
  
  const pastors = [
    { id: 1, 
        name: 'Pr Henrique\nPereira', 
        photo: `${pathBase}photos/people/henrique.png`, 
        bio: `Henrique Pereira é o pastor principal da nossa igreja e lidera com um coração cheio de alegria, humildade e dedicação ao serviço de Deus e das pessoas. Casado com Minita Pereira, são pais da Rute e do Marcos — que é casado com a Myriam — e avós orgulhosos da pequena Noa, a alegria da família.

        A sua jornada no ministério começou em 1989, ao lado da sua esposa, quando ambos serviram como pastores assistentes. Ao longo dos anos, têm sido uma presença constante na vida da comunidade, e em 2022 assumiram a liderança pastoral principal da igreja.

        O Pastor Henrique é conhecido pela sua proximidade com as pessoas, pela forma simples mas profunda como comunica a Palavra de Deus, e por ser alguém que ouve, cuida e caminha ao lado de quem o procura. A sua paixão é ver vidas transformadas pelo amor de Jesus — pessoas que descobrem que têm valor, propósito e um lugar na família de Deus. Para ele, a igreja deve ser um espaço onde todos são bem-vindos, independentemente do passado, onde há crescimento espiritual genuíno e onde a transformação acontece através do poder do Evangelho e da vivência em comunidade.`, 
        spouseId: 2 },
    { id: 2, 
        name: 'Pra Minita\nPereira',  
        photo: `${pathBase}photos/people/minita.png`, 
        bio: `Minita Pereira é esposa do Pastor Henrique e uma líder dedicada e inspiradora no seio da igreja. Com um coração cheio de empatia, sabedoria e sensibilidade espiritual, tem sido uma figura essencial na caminhada pastoral da comunidade desde 1989.

        Ao longo dos anos, Minita tem acompanhado muitas pessoas nas suas jornadas de fé, especialmente mulheres e famílias, com uma presença firme e encorajadora. É alguém que sabe escutar com atenção, orar com fé e apoiar com amor — sempre com um sorriso acolhedor e palavras de esperança.

        Enquanto mulher de fé, mãe e avó, Minita vive o ministério com naturalidade, integrando o cuidado da família com o cuidado da igreja. A sua vida é um reflexo do amor de Cristo em ação — discreta mas marcante, simples mas profunda. A sua visão, alinhada com a do Pastor Henrique, é ver uma igreja viva, acolhedora e centrada em Jesus — um lugar onde todos podem crescer, restaurar-se e descobrir o seu papel no plano de Deus.`, 
        spouseId: 1 },
    { id: 3, 
        name: 'Pr Rogério\nTrindade', 
        photo: `${pathBase}photos/people/rog.png`, 
        bio: 
        `   Rogério Trindade é casado com a Johana Antelo e têm dois filhos, o John e a Zoé. Nasceu na África do Sul, na cidade de Johanesburgo, fazendo parte de uma família de emigrantes portugueses e de cristãos comprometidos no serviço. 

        Foi pastor titular durante 3 anos de uma igreja evangélica local em Espanha, na cidade de Sevilha. É pastor auxiliar na ICMAV desde 2016. É Líder-coordenador da ICMAV com Propósitos e dos Ministérios de Ligação. É também Diretor e formador da ICMAV COLLEGE. Foi fundador da Escola de Liderança com Propósitos (LCP) em 2015, nome anterior da escola. É autor de mais de 30 manuais de treinamento para líderes.`, 
        spouseId: 4 },
    { id: 4, name: 'Pra Johana\nVillarroel', photo: `${pathBase}photos/people/johana.png`, bio: '…', spouseId: 3 },
    { id: 5, name: 'Pr Manza\nGarcia',     photo: `${pathBase}photos/people/manza.png`, bio: 
        `   O Pr. Manza Garcia nasceu na República Democrática do Congo. Com 19 anos foi para Angola onde frequentou uma igreja baptista onde serviu a Deus como cantor durante 3 anos. A seguir foi para o sul de Angola durante 2 anos, voltando depois para Luanda onde começou o ministério como evangelista a pregar na igreja e em campanhas de massas com centenas de pessoas.
        
        Em 1989 veio para Portugal onde fundou uma igreja junto com uns amigos, onde ficou até 1995 quando o Pr. Leitão da igreja de Cascais o convidou para vir para a ICMAV, onde actualmente serve como pastor em Cascais e no Monte da Caparica.
        
        A ICMAV é uma igreja que está no seu coração, sendo uma comunidade que é relevante e que serve a Deus estendendo o Reino de Deus aqui na Terra. Acredita que a igreja não é para ser pequena, mas para crescer e continuar a ganhar espaço, querendo contribuir para esta expansão do Reino de Deus aqui na Terra na sua forma espiritual e física.` },
    { id: 6, 
        name: 'Pr Paulo João\nCorreia',
        photo: `${pathBase}photos/people/pj.png`,    
        bio: 
        `   Paulo João é pastor de louvor e adoração na ICMAV, onde também lidera o ministério de homens. Casado com Denise, é pai de dois filhos e avô da Salomé. 
            
        A sua jornada no ministério começou aos 14 anos, após um encontro marcante com Jesus. Durante 18 anos serviu no Desafio Jovem, desenvolvendo trabalho evangelístico e social junto de comunidades vulneráveis e pessoas em situação de dependência.
            
        Desde 2006, dedica-se a tempo inteiro ao ministério pastoral, com ênfase no louvor, na formação de novas gerações e no discipulado de homens. A paternidade e a cultura do Reino no seio familiar são temas centrais da sua missão, procurando levantar líderes que vivam segundo o coração de Deus.`, spouseId: 7 },
    { id: 7, 
        name: 'Pra Denise\nCorreia',  
        photo: `${pathBase}photos/people/denise.png`, 
        bio: `É esposa do Pastor Paulo João e tem sido, desde o início, uma companheira incansável no ministério. Embora não esteja à frente da adoração, a sua presença discreta e constante tem sido fundamental ao longo de toda a caminhada pastoral da família. Desde muito jovem, partilhou com o Paulo o chamado para servir, caminhando ao seu lado em todas as fases — desde os primeiros passos no ministério aos 14 anos, passando pelos anos intensos no Desafio Jovem, até ao serviço pastoral a tempo inteiro iniciado em 2006.

Mãe de dois filhos e avó da pequena Salomé, Denise vive o seu ministério com o coração voltado para a família, o cuidado das pessoas e a edificação da Igreja. É uma mulher de oração, sensível à voz de Deus, e uma referência silenciosa de força, fé e dedicação. A sua missão não passa pelos holofotes, mas pela fidelidade no dia a dia, sempre disponível, sempre presente, sempre a semear amor.`, 
        spouseId: 6 },
    { id: 8, 
        name: 'Pr Danilo\nGujral',    
        photo: `${pathBase}photos/people/danilo.png`, 
        bio: 
        `   Nascido em Moçambique casado com Havani Gujral, pastor na ICMAV desde 2006 tendo já  ocupado várias areas de ministério na igreja. Atualmente eles são  responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até  ao Batismo nas Águas ou Membresia na Igreja. 

        Também supervisionam e treinam para o ministério  das várias equipas do Celebrando Restauração da ICMAV.  É produtor do programa  radiofónico "Ponto de Encontro" dirigido aos solteiros, divorciados e viúvos uma parceria com a Rádio Transmundial de Portugal.`, 
        spouseId: 9 },
    { id: 9, name: 'Pra Havani\nGujral',   
        photo: `${pathBase}photos/people/havani.png`, 
        bio:         
        `   Nascida no Brasil casada com Danilo Gujral, pastora na ICMAV desde 2006.

        Atualmente eles são  responsáveis pelas várias equipas ligadas ao Propósito PERTENCER, que acompanham e apoiam quem nos visita até  ao Batismo nas Águas ou Membresia na Igreja.
        
        Também supervisionam e treinam para o ministério  das várias equipas do Celebrando Restauração da ICMAV.`, 
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
  