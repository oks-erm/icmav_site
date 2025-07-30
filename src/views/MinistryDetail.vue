<!-- src/views/MinistryDetail.vue -->
<template>
  <div class="flex flex-col min-h-screen">
      <div class="max-w-350 mx-auto h-auto py-16 px-12 flex-grow" data-aos="fade-up">
      <!-- Back button -->
      <button @click="$router.back()" class="btn btn-ghost mb-8">
        ← Voltar
      </button>

      <!-- Title  -->
      <div class="flex flex-row md:flex-row items-center justify-center mb-6">
        <h1 class="text-4xl font-bold mr-2">{{ ministry.name }}</h1>
      </div>

      <!-- 2-col layout -->
        <div class="grid grid-cols-5 gap-3 md:gap-8 mb-12 items-start auto-rows-min">
        <!-- Left media -->
        <div class="col-span-5 md:col-span-2">
          <div class="relative">
            <!-- Hero Image - shown as placeholder while video loads, or if no video -->
            <img
              :src="ministry.media.placeholder"
              alt="Ministry placeholder"
              class="w-full rounded-lg shadow-lg transition-opacity duration-500 relative z-10"
              :class="{ 
                'opacity-100': !hasVideo || !isVideoLoaded || videoError,
                'opacity-0': hasVideo && isVideoLoaded && !videoError 
              }"
            />
            
            <!-- Video with device detection - only if video source exists -->
            <video
              v-if="hasVideo"
              ref="ministryVideo"
              :src="getMinistryVideoSource(ministry.media.src)"
              autoplay
              muted
              loop
              playsinline
              preload="auto"
              class="absolute inset-0 w-full rounded-lg shadow-lg transition-opacity duration-500 z-20"
              :class="{ 
                'opacity-100': isVideoLoaded && !videoError,
                'opacity-0': !isVideoLoaded || videoError 
              }"
              @loadeddata="handleVideoLoaded"
              @error="handleVideoError"
            >
              Your browser does not support the <code>video</code> element.
            </video>
          </div>
          
          <div class="flex mt-6 ">
            <p class="text-l md:text-xl">Segue-nos nas redes sociais:</p>
          <a
            v-for="(s, i) in ministry.socialMedia"
            :key="i"
            :href="s.link"
            target="_blank"
            class="w-12 h-12 px-3 flex rounded-full text-3xl text-primary hover:bg-base-300 transition"
            style="margin-bottom: -3px;"
          >
            <i :class="s.icon"></i>
          </a>
        </div>
        </div>

        <!-- Right description -->
        <div class="prose text-base-content/90 col-span-5 md:col-span-3">
          <p
            v-for="(para, i) in ministry.longDescription"
            :key="i"
            class="py-2"
          >
            {{ para }}
          </p>

          <!-- Leader info -->
          <div class="flex !flex-col items-center mt-8 space-y-4 md:space-y-0 ">
            <img
              :src="ministry.leaderPhoto"
              :alt="ministry.leader"
              class="w-24 h-24 rounded-full object-cover shadow-lg mb-2"
            />
            <div class="text-center">
              <div class="flex flex-col items-center justify-center md:justify-start">
                <div class="badge badge-sm badge-primary">Líder</div>
                <div class="font-bold text-lg">{{ ministry.leader }}</div>
              </div>
              <p v-if="ministry.contact" class="text-sm">{{ ministry.contact }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- page footer -->
    <Footer />
  </div>
</template>
  
<script setup>
import { computed, ref } from 'vue'
import Footer from '../components/Footer.vue'
import { useRoute, useRouter } from 'vue-router'

const route  = useRoute()
const router = useRouter()

const isVideoLoaded = ref(false)
const videoError = ref(false)
const ministryVideo = ref(null)

// Check if current ministry has video
const hasVideo = computed(() => {
  return ministry.value?.media?.type === 'video' && ministry.value?.media?.src
})

// Device detection function
function getDeviceType() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera
    
    if (/android/i.test(userAgent) || /iPad|iPhone|iPod/.test(userAgent)) {
        return 'mobile'
    }
    
    if (/tablet|ipad/i.test(userAgent)) {
        return 'mobile'
    }
    
    return 'desktop'
}

// Get appropriate video source based on device
function getMinistryVideoSource(baseSrc) {
    const deviceType = getDeviceType()
    let finalSrc = baseSrc

    if (deviceType === 'mobile') {
        finalSrc = baseSrc.replace('-desktop-720.mp4', '-mobile-360.mp4')
    }
    
    console.log(`Loading video: ${finalSrc} for device: ${deviceType}`)
    return finalSrc
}

function handleVideoLoaded() {
    console.log('Video loaded successfully')
    isVideoLoaded.value = true
    videoError.value = false
}

function handleVideoError(event) {
    console.error('Video failed to load:', event.target.src)
    
    // If mobile video failed, try fallback to desktop version
    const currentSrc = event.target.src
    if (currentSrc.includes('-mobile.mp4')) {
        console.log('Mobile video failed, trying desktop version...')
        const desktopSrc = currentSrc.replace('-mobile.mp4', '-desktop.mp4')
        event.target.src = desktopSrc
        return
    }
    
    console.log('All video sources failed, showing placeholder image')
    videoError.value = true
    isVideoLoaded.value = false
}

// Update MINISTRIES data to use device-specific naming
const MINISTRIES = [
  {
    slug: 'criancas',
    name: 'ICMAV Crianças / Alfa',
    media: {
      type: 'video',
      src: `/videos/hero.mp4`, // Will become hero-desktop-1080.mp4 or hero-mobile-480.mp4
      placeholder: `/fallbacks/criancas.png`
    },
    longDescription: [
        'O ministério das crianças é um espaço cheio de alegria, criatividade e crescimento. Em cada encontro, as crianças são convidadas a mergulhar nas histórias da Bíblia de forma divertida e acessível — através de teatro, música, jogos e atividades que despertam a imaginação e mostram, de forma simples e verdadeira, o amor de Deus.',
        'Durante a série ALFA Kids, promovemos momentos especiais que envolvem tanto as crianças como os pais. São experiências pensadas para fortalecer os laços familiares e, ao mesmo tempo, lançar as bases da fé no coração dos mais novos. Acreditamos que a caminhada com Deus começa em casa e queremos caminhar ao lado das famílias nesse processo.',
        'Para além dos encontros semanais, organizamos também eventos temáticos em datas especiais como a Páscoa, o Natal ou o Dia da Criança. Tudo acontece num ambiente seguro, acolhedor e com uma equipa dedicada que cuida, ensina e brinca com os mais pequenos com muito carinho.',
    ],
    leader: 'Patricia Pinto',
    leaderPhoto: `/photos/people/patricia.jpg`,
    contact: '(+351) 913 300 792',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/alfa.icmav' }
    ]
  },
  {
    slug: 'teens',
    name: 'ICMAV Teens',
    media: {
      type: 'video',
      src: `/videos/teens-desktop-720.mp4`, // Will become teens-mobile-360.mp4 on mobile
      placeholder: `/fallbacks/teens.png`
    },
    longDescription: [
        'O grupo Teens é um espaço vibrante, pensado especialmente para adolescentes que estão a descobrir quem são e em que acreditam. Aqui, combinamos momentos de louvor, conversas reais e oficinas criativas que incentivam a expressão pessoal, sempre com base em princípios cristãos.',
        'Queremos criar um ambiente onde cada jovem se sinta valorizado, ouvido e desafiado a crescer — não só na fé, mas também nas relações, no caráter e nas escolhas do dia a dia.',
        'Ao longo do ano, organizamos retiros, encontros temáticos e iniciativas solidárias que desenvolvem a liderança, o espírito de equipa e o sentido de missão. É uma oportunidade única para fazer amigos, servir, descobrir o propósito pessoal e aprender a viver com responsabilidade e intencionalidade.',
    ],
    leader: 'João Maria Guedelha',
    leaderPhoto: `/photos/people/joao-maria.jpg`,
    contact: '(+351) 933 838 746',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icteens' }
    ]
  },
  {
    slug: 'jovens',
    name: 'ICMAV Jovens',
    media: {
      type: 'image',
      src: null,
      placeholder: `/fallbacks/jovens.png`
    },
    longDescription: [
        'Os encontros de Jovens juntam pessoas dos 18 aos 30 anos num ambiente descontraído, cheio de propósito. São momentos marcados por adoração, estudo da Palavra e partilha de vida — um espaço seguro para fazer perguntas, crescer na fé e construir amizades verdadeiras.',
        'Queremos inspirar esta geração a viver uma fé viva e prática, que se reflete nas escolhas diárias, no trabalho, na universidade, em casa e nas relações. Acreditamos que seguir Jesus é uma aventura transformadora que começa no coração e impacta tudo à volta.',
        'Para além dos encontros quinzenais, dinamizamos seminários, missões urbanas e outros eventos que fortalecem a ligação com Deus e com a cidade. Cada jovem é desafiado a descobrir o seu chamado e a ser luz onde quer que esteja — com coragem, criatividade e compaixão.',
    ],
    leader: 'Marcos Pereira',
    leaderPhoto: `/photos/people/marcos.jpg`,
    contact: '(+351) 912 847 221',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icyouth' }
    ]
  },
  {
    slug: 'homens',
    name: 'ICMAV Homens',
    media: {
      type: 'video',
      src: `/videos/homens-desktop-720.mp4`, // This exists as-is, no device-specific versions
      placeholder: `/fallbacks/homens.jpg`
    },
    longDescription: [
        'O ministério de Homens é um espaço onde homens de todas as idades se juntam para crescer na fé e nas relações uns com os outros. Através de estudos bíblicos, conversas honestas e atividades ao ar livre, queremos promover uma caminhada cristã autêntica, com foco no discipulado e no fortalecimento da identidade em Cristo.',
        'Mais do que encontros pontuais, este ministério é uma rede de apoio e amizade. Organizamos retiros, caminhadas, pequenos-almoços e grupos de partilha onde os homens podem abrir o coração, partilhar lutas e celebrar vitórias num ambiente de confiança, respeito e encorajamento mútuo.',
        'Acreditamos que cada homem tem um papel essencial na família, na igreja e na sociedade — e queremos ser parte ativa no processo de crescimento espiritual, emocional e relacional de cada um.',
    ],
    leader: 'Paulo João Correia',
    leaderPhoto: `/photos/people/pj.jpg`,
    contact: '(+351) 919 947 770',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_homens' }
    ]
  },
  {
    slug: 'mulheres',
    name: 'ICMAV Mulheres',
    media: {
      type: 'image',
      src: null,
      placeholder: `/fallbacks/mulheres.png`
    },
    longDescription: [
        'O ministério de Mulheres é um espaço pensado para acolher, encorajar e fortalecer mulheres em todas as fases da vida. Através de estudos bíblicos, oração e partilha, criamos um ambiente seguro onde cada mulher pode crescer na fé, aprofundar a sua relação com Deus e construir amizades significativas.',
        'Os nossos encontros incluem workshops, palestras, tempos de louvor e eventos especiais que tocam em temas relevantes do dia a dia — sempre com o objetivo de trazer inspiração, cura, renovação e um sentido mais profundo de propósito.',
        'Acreditamos que cada mulher tem um valor único e uma chamada divina, e queremos caminhar juntas nesta jornada, apoiando-nos umas às outras com graça, verdade e alegria.',
    ],
    leader: 'Cristina Silva',
    leaderPhoto: `/photos/people/cristina.jpg`,
    contact: '(+351) 969 817 059',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_mulheres' }
    ]
  },
  {
    slug: 'casais',
    name: 'ICMAV Casais',
    media: {
      type: 'image',
      src: null,
      placeholder: `/fallbacks/casais.png`
    },
    longDescription: [
        'O ministério de Casais existe para apoiar e fortalecer os relacionamentos, ajudando cada casal a crescer em amor, unidade e propósito. Promovemos encontros com temas relevantes, palestras, momentos de oração e dinâmicas práticas baseadas nos princípios da Palavra de Deus.',
        'Acreditamos que um casamento saudável não acontece por acaso — é construído com intencionalidade, comunicação e graça. Por isso, oferecemos acompanhamento pastoral, aconselhamento e espaços de partilha onde os casais podem aprender, rir, chorar e crescer juntos.',
        'Também organizamos conferências e retiros especiais que proporcionam tempo de qualidade a dois, ferramentas para lidar com desafios e oportunidades para renovar os votos e a visão do casamento. Queremos ver famílias fortes, resilientes e cheias de fé a impactar o mundo à sua volta.',
    ],
    leader: 'Pedro Mateus',
    leaderPhoto: `/photos/people/pedro-mateus.jpg`,
    contact: '(+351) 916 686 956',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_casais' }
    ]
  }
]

const ministry = computed(() =>
  MINISTRIES.find(m => m.slug === route.params.slug)
)

if (!ministry.value) {
  router.replace({ name: 'Home' })
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
