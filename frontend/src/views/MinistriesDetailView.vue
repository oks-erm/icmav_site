<!-- src/views/MinistriesDetailView.vue -->

<template>
  <div class="flex flex-col min-h-screen bg-gray-50">
    <!-- Sticky Header -->
    <StickyHeader />

    <main class="flex-grow py-10 sm:py-14 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto w-full">
      <!-- Estado de Carregamento -->
      <div v-if="loading && !ministry" class="space-y-6 animate-pulse">
        <div class="h-12 bg-gray-200 rounded-2xl w-2/3 max-w-md"></div>
        <div class="h-96 bg-gray-200 rounded-3xl"></div>
        <div class="h-80 bg-gray-200 rounded-3xl"></div>
      </div>

      <!-- Ministério não encontrado -->
      <div v-else-if="!ministry" class="text-center py-20 bg-white rounded-3xl shadow-sm border border-gray-100 p-8">
        <i class="fa-solid fa-circle-exclamation text-5xl text-gray-400 mb-4"></i>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Ministério não encontrado</h2>
        <p class="text-gray-500 mb-6">O ministério que procuras não existe ou foi atualizado.</p>
        <router-link
          to="/"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-primary text-white font-semibold shadow hover:bg-primary/90 transition-all"
        >
          <span>Ir para o Início</span>
        </router-link>
      </div>

      <!-- Conteúdo do Ministério: 1. Topo -> 2. Sobre -> 3. Média -> 4. Redes Sociais -->
      <div v-else class="space-y-8" data-aos="fade-up">
        <!-- 1. Topo: Ícone, Título e Descrição Curta -->
        <div class="space-y-3 text-center sm:text-left">
          <div class="flex items-center justify-center sm:justify-start gap-3">
            <span
              v-if="ministry.icon"
              class="w-12 h-12 rounded-2xl flex items-center justify-center text-white text-xl shadow-md"
              :class="ministry.bgClass || 'bg-primary'"
            >
              <i :class="ministry.icon"></i>
            </span>
            <span class="text-xs uppercase tracking-widest font-bold text-primary">Ministério ICMAV</span>
          </div>

          <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-900 tracking-tight">
            {{ ministry.name }}
          </h1>

          <p v-if="ministry.desc" class="text-lg sm:text-xl text-gray-600 max-w-3xl leading-relaxed">
            {{ ministry.desc }}
          </p>
        </div>

        <!-- 2. Secção "Sobre o Ministério" (primeiro) -->
        <div class="w-full bg-white rounded-3xl p-8 sm:p-12 shadow-xl border border-gray-100 space-y-8">
          <div class="border-b border-gray-100 pb-4">
            <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">Sobre o Ministério</h2>
          </div>

          <!-- Parágrafos da Descrição Longa -->
          <div class="space-y-5 text-gray-700 leading-relaxed text-base sm:text-lg">
            <template v-if="Array.isArray(ministry.longDescription)">
              <p v-for="(para, i) in ministry.longDescription" :key="i">
                {{ para }}
              </p>
            </template>
            <template v-else-if="ministry.longDescription">
              <p>{{ ministry.longDescription }}</p>
            </template>
            <template v-else>
              <p class="text-gray-500 italic">Informação detalhada em atualização.</p>
            </template>
          </div>

          <!-- Cartão do Líder -->
          <div class="pt-6 border-t border-gray-100">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 p-6 rounded-2xl bg-gray-50 border border-gray-100">
              <img
                v-if="ministry.leaderPhoto"
                :src="ministry.leaderPhoto"
                :alt="ministry.leader || 'Líder'"
                loading="lazy"
                decoding="async"
                class="w-20 h-20 sm:w-24 sm:h-24 rounded-full object-cover shadow-md ring-4 ring-primary/20 flex-shrink-0"
              />
              <div
                v-else
                class="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-primary/10 text-primary flex items-center justify-center text-3xl font-bold flex-shrink-0 ring-4 ring-primary/20"
              >
                <i class="fa-solid fa-user"></i>
              </div>

              <div class="text-center sm:text-left space-y-1.5 flex-grow">
                <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-primary text-white">
                  Líder Responsável
                </span>
                <h3 class="text-xl sm:text-2xl font-bold text-gray-900">
                  {{ ministry.leader || 'Equipa de Liderança' }}
                </h3>

                <div v-if="ministry.contact" class="pt-1">
                  <a
                    :href="ministry.contact.startsWith('+') ? `tel:${ministry.contact}` : `mailto:${ministry.contact}`"
                    class="inline-flex items-center gap-2 text-sm sm:text-base text-gray-600 hover:text-primary transition-colors font-medium"
                  >
                    <i class="fa-solid fa-phone text-xs text-primary"></i>
                    <span>{{ ministry.contact }}</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Secção Multimédia (Foto ou Vídeo na largura total da secção - depois do Sobre) -->
        <div class="w-full rounded-3xl shadow-xl overflow-hidden bg-black border border-gray-100">
          <!-- Caso seja Vídeo -->
          <div
            v-if="ministry.media?.type === 'video' && ministry.media?.src"
            class="relative w-full aspect-video flex items-center justify-center bg-black"
          >
            <video
              :src="ministry.media.src"
              controls
              autoplay
              muted
              loop
              playsinline
              class="w-full h-full object-cover"
            >
              O teu navegador não suporta a reprodução de vídeo.
            </video>
          </div>

          <!-- Caso seja Imagem -->
          <div
            v-else
            class="relative w-full aspect-video sm:aspect-[16/9] flex items-center justify-center bg-gray-100"
          >
            <img
              :src="ministry.media?.src || ministry.media?.placeholder || '/src/assets/fallbacks/hero.jpg'"
              :alt="ministry.name"
              loading="lazy"
              decoding="async"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

        <!-- 4. Secção Redes Sociais (por fim) -->
        <div
          v-if="ministry.socialMedia && ministry.socialMedia.length"
          class="w-full bg-white rounded-3xl p-6 sm:p-8 shadow-md border border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4"
        >
          <div class="text-center sm:text-left">
            <h3 class="text-base sm:text-lg font-bold text-gray-900">
              Segue o ministério nas redes sociais
            </h3>
            <p class="text-sm text-gray-500">Acompanha as atividades e novidades exclusivas deste grupo.</p>
          </div>

          <div class="flex flex-wrap gap-3">
            <a
              v-for="(s, i) in ministry.socialMedia"
              :key="i"
              :href="s.link"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2.5 px-5 py-3 rounded-2xl bg-gray-50 hover:bg-primary/10 text-gray-700 hover:text-primary transition-all text-sm font-semibold border border-gray-200 shadow-sm"
            >
              <i :class="[s.icon, 'text-xl text-primary']"></i>
              <span>{{ getSocialName(s.icon) }}</span>
            </a>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import StickyHeader from '../components/StickyHeader.vue'
import Footer from '../components/Footer.vue'
import { getMinistriesPresentationContent } from '../services/api'

const route = useRoute()
const loading = ref(true)
const ministriesList = ref([])

// Fallback local caso o backend ainda não tenha sido populado
const FALLBACK_MINISTRIES = [
  {
    slug: 'criancas',
    name: 'ICMAV Crianças / Alfa',
    icon: 'fas fa-hands-holding-child',
    bgClass: 'bg-accent',
    desc: 'Aqui a imaginação voa e o coração aprende o que realmente importa.',
    media: {
      type: 'video',
      src: '/src/assets/videos/hero.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'O ministério das crianças é um espaço cheio de alegria, criatividade e crescimento. Em cada encontro, as crianças são convidadas a mergulhar nas histórias da Bíblia de forma divertida e acessível — através de teatro, música, jogos e atividades que despertam a imaginação e mostram, de forma simples e verdadeira, o amor de Deus.',
      'Durante a série ALFA Kids, promovemos momentos especiais que envolvem tanto as crianças como os pais. São experiências pensadas para fortalecer os laços familiares e, ao mesmo tempo, lançar as bases da fé no coração dos mais novos. Acreditamos que a caminhada com Deus começa em casa e queremos caminhar ao lado das famílias nesse processo.',
      'Para além dos encontros semanais, organizamos também eventos temáticos em datas especiais como a Páscoa, o Natal ou o Dia da Criança. Tudo acontece num ambiente seguro, acolhedor e com uma equipa dedicada que cuida, ensina e brinca com os mais pequenos com muito carinho.',
    ],
    leader: 'Patricia Pinto',
    leaderPhoto: '/src/assets/photos/people/patricia.png',
    contact: '+351 912 000 111',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/alfa.icmav' },
    ],
  },
  {
    slug: 'teens',
    name: 'ICMAV Teens',
    icon: 'fas fa-music',
    bgClass: 'bg-primary',
    desc: 'Aqui é onde começa a tua jornada: com gente real e fé prática.',
    media: {
      type: 'video',
      src: '/src/assets/videos/teens.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'O grupo Teens é um espaço vibrante, pensado especialmente para adolescentes que estão a descobrir quem são e em que acreditam. Aqui, combinamos momentos de louvor, conversas reais e oficinas criativas que incentivam a expressão pessoal, sempre com base em princípios cristãos.',
      'Queremos criar um ambiente onde cada jovem se sinta valorizado, ouvido e desafiado a crescer — não só na fé, mas também nas relações, no caráter e nas escolhas do dia a dia.',
      'Ao longo do ano, organizamos retiros, encontros temáticos e iniciativas solidárias que desenvolvem a liderança, o espírito de equipa e o sentido de missão. É uma oportunidade única para fazer amigos, servir, descobrir o propósito pessoal e aprender a viver com responsabilidade e intencionalidade.',
    ],
    leader: 'João Maria Guedelha',
    leaderPhoto: '/src/assets/photos/people/joao-maria.png',
    contact: '+351 912 000 222',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icteens' },
    ],
  },
  {
    slug: 'jovens',
    name: 'ICMAV Jovens',
    icon: 'fas fa-heart',
    bgClass: 'bg-secondary',
    desc: 'Bora lá viver que vai além do comum, com propósito e significado.',
    media: {
      type: 'video',
      src: '/src/assets/videos/hero.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'Os encontros de Jovens juntam pessoas dos 18 aos 30 anos num ambiente descontraído, cheio de propósito. São momentos marcados por adoração, estudo da Palavra e partilha de vida — um espaço seguro para fazer perguntas, crescer na fé e construir amizades verdadeiras.',
      'Queremos inspirar esta geração a viver uma fé viva e prática, que se reflete nas escolhas diárias, no trabalho, na universidade, em casa e nas relações. Acreditamos que seguir Jesus é uma aventura transformadora que começa no coração e impacta tudo à volta.',
      'Para além dos encontros quinzenais, dinamizamos seminários, missões urbanas e outros eventos que fortalecem a ligação com Deus e com a cidade. Cada jovem é desafiado a descobrir o seu chamado e a ser luz onde quer que esteja — com coragem, criatividade e compaixão.',
    ],
    leader: 'Marcos Pereira',
    leaderPhoto: '/src/assets/photos/people/marcos.png',
    contact: '+351 912 000 333',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icyouth' },
    ],
  },
  {
    slug: 'homens',
    name: 'ICMAV Homens',
    icon: 'fas fa-hands-helping',
    bgClass: 'bg-warning',
    desc: 'Grupo de camaradagem, troca e crescimento para todas as fases da vida .',
    media: {
      type: 'video',
      src: '/src/assets/videos/hero.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'O ministério de Homens é um espaço onde homens de todas as idades se juntam para crescer na fé e nas relações uns com os outros. Através de estudos bíblicos, conversas honestas e atividades ao ar livre, queremos promover uma caminhada cristã autêntica, com foco no discipulado e no fortalecimento da identidade em Cristo.',
      'Mais do que encontros pontuais, este ministério é uma rede de apoio e amizade. Organizamos retiros, caminhadas, pequenos-almoços e grupos de partilha onde os homens podem abrir o coração, partilhar lutas e celebrar vitórias num ambiente de confiança, respeito e encorajamento mútuo.',
      'Acreditamos que cada homem tem um papel essencial na família, na igreja e na sociedade — e queremos ser parte ativa no processo de crescimento espiritual, emocional e relacional de cada um.',
    ],
    leader: 'Paulo João Correia',
    leaderPhoto: '/src/assets/photos/people/pj.png',
    contact: '+351 912 000 444',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_homens' },
    ],
  },
  {
    slug: 'mulheres',
    name: 'ICMAV Mulheres',
    icon: 'fas fa-female',
    bgClass: 'bg-info',
    desc: 'Um grupo de mulheres que merece um espaço onde é ouvida, valorizada e encorajada.',
    media: {
      type: 'video',
      src: '/src/assets/videos/hero.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'O ministério de Mulheres é um espaço pensado para acolher, encorajar e fortalecer mulheres em todas as fases da vida. Através de estudos bíblicos, oração e partilha, criamos um ambiente seguro onde cada mulher pode crescer na fé, aprofundar a sua relação com Deus e construir amizades significativas.',
      'Os nossos encontros incluem workshops, palestras, tempos de louvor e eventos especiais que tocam em temas relevantes do dia a dia — sempre com o objetivo de trazer inspiração, cura, renovação e um sentido mais profundo de propósito.',
      'Acreditamos que cada mulher tem um valor único e um chamado divino, e queremos caminhar juntas nesta jornada, apoiando-nos umas às outras com graça, verdade e alegria.',
    ],
    leader: 'Cristina Silva',
    leaderPhoto: '/src/assets/photos/people/cristina.png',
    contact: '+351 912 000 555',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_mulheres' },
    ],
  },
  {
    slug: 'casais',
    name: 'ICMAV Casais',
    icon: 'fas fa-globe',
    bgClass: 'bg-error',
    desc: 'Porque cuidar do relacionamento a dois também é uma forma de amar.',
    media: {
      type: 'video',
      src: '/src/assets/videos/hero.mp4',
      placeholder: '/src/assets/fallbacks/hero.jpg',
    },
    longDescription: [
      'O ministério de Casais existe para apoiar e fortalecer os relacionamentos, ajudando cada casal a crescer em amor, unidade e propósito. Promovemos encontros com temas relevantes, palestras, momentos de oração e dinâmicas práticas baseadas nos princípios da Palavra de Deus.',
      'Acreditamos que um casamento saudável não acontece por acaso — é construído com intencionalidade, comunicação e graça. Por isso, oferecemos acompanhamento pastoral, aconselhamento e espaços de partilha onde os casais podem aprender, rir, chorar e crescer juntos.',
      'Também organizamos conferências e retiros especiais que proporcionam tempo de qualidade a dois, ferramentas para lidar com desafios e oportunidades para renovar os votos e a visão do casamento. Queremos ver famílias fortes, resilientes e cheias de fé a impactar o mundo à sua volta.',
    ],
    leader: 'Pedro Mateus',
    leaderPhoto: '/src/assets/photos/people/pedro-mateus.png',
    contact: '+351 912 000 666',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_casais' },
    ],
  },
]

const ministry = computed(() => {
  const slug = route.params.slug
  if (!slug) return null

  // 1. Procurar na lista carregada da API
  const fromApi = ministriesList.value.find((m) => m.slug === slug)
  if (fromApi) return fromApi

  // 2. Fallback para dados locais estruturados
  return FALLBACK_MINISTRIES.find((m) => m.slug === slug) || null
})

function getSocialName(icon) {
  if (!icon) return 'Social'
  if (icon.includes('instagram')) return 'Instagram'
  if (icon.includes('facebook')) return 'Facebook'
  if (icon.includes('youtube')) return 'YouTube'
  if (icon.includes('tiktok')) return 'TikTok'
  return 'Rede Social'
}

async function loadData() {
  loading.value = true
  try {
    const res = await getMinistriesPresentationContent()
    if (res && Array.isArray(res.value)) {
      ministriesList.value = res.value
    }
  } catch {
    // Utiliza fallback silenciosamente
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
  window.scrollTo({ top: 0, behavior: 'instant' })
})
</script>

<style scoped>
</style>