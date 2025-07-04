<!-- src/views/MinistryDetail.vue -->
<template>
    <div class="flex flex-col min-h-screen">
    <div class="max-w-350 mx-auto h-auto py-16 px-12 flex-grow" data-aos="fade-up">
      <!-- Back button -->
      <button @click="$router.back()" class="btn btn-ghost mb-8">
        ← Voltar
      </button>
  
      <!-- Title + social (inline) -->
      <div class="flex flex-row md:flex-row items-center justify-center mb-6">
        <h1 class="text-4xl font-bold mr-2">{{ ministry.name }}</h1>
        <div class="flex space-x-4">
          <a
            v-for="(s, i) in ministry.socialMedia"
            :key="i"
            :href="s.link"
            target="_blank"
            class="w-12 h-12 flex items-center justify-center rounded-full text-3xl text-primary hover:bg-base-300 transition"
            style="margin-bottom: -3px;"
          >
            <i :class="s.icon"></i>
          </a>
        </div>
      </div>
  
      <!-- 2-column layout: video left, text right -->
      <div class="grid grid-cols-5 gap-8 mb-12 items-start">
        <!-- Left: Hero Video Placeholder -->
        <div class="col-span-2">
          <video
            src="/src/assets/hero.mp4"
            controls
            autoplay
            muted
            loop
            playsinline
            class="w-full h-100 rounded-lg shadow-lg"
          >
            Your browser does not support the <code>video</code> element.
          </video>
        </div>
  
        <!-- Right: Rich Description -->
        <div class="prose text-base-content/90 col-span-3">
          <p v-for="(para, i) in ministry.longDescription" :key="i">
            {{ para }}
          </p>
        <div class="flex flex-col md:flex-row items-center mb-8 mt-8">
        <img
          :src="ministry.leaderPhoto"
          :alt="ministry.leader"
          class="w-24 h-24 rounded-full object-cover shadow-lg mr-0 md:mr-4 mb-4 md:mb-0"
        />
        <div class="text-center md:text-left">
          <p class="flex items-center justify-center md:justify-start space-x-2">
            <span class="badge badge-sm badge-primary">Líder</span>
            <span class="font-bold text-lg">{{ ministry.leader }}</span>
          </p>
          <p v-if="ministry.contact" class="text-sm">{{ ministry.contact }}</p>
        </div>
      </div>
        </div>
      </div>
    </div>
    <Footer />
</div>

  </template>
  
  
  <script setup>
  import { computed } from 'vue'
  import Footer from '../components/Footer.vue'
  import { useRoute, useRouter } from 'vue-router'
  
  const route  = useRoute()
  const router = useRouter()
  
  const MINISTRIES = [
  {
    slug: 'criancas',
    name: 'ICMAV Crianças / Alfa',
    media: { type: 'image', src: 'src/assets/criancas.png' },
    longDescription: [
      'O ministério de Crianças é cheio de alegria e descobertas. A cada encontro, contamos histórias bíblicas por meio de teatro, música e brincadeiras que ajudam os pequenos a conhecerem o amor de Deus.',
      'Na série ALFA Kids, promovemos atividades criativas que envolvem pais e filhos juntos, fortalecendo laços familiares e plantando sementes de fé no coração das gerações mais jovens.',
      'Além dos encontros semanais, realizamos eventos especiais em datas comemorativas, garantindo um ambiente seguro e acolhedor para todas as crianças.',
   ],
    leader: 'Patricia Pinto',
    leaderPhoto: 'src/assets/patricia.png',
    contact: '+351 912 000 111',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/alfa.icmav' }
    ]
  },
  {
    slug: 'teens',
    name: 'ICMAV Teens',
    media:   { type: 'image', src: 'src/assets/teens.png' },
    longDescription: [
      'O grupo Teens é um espaço vibrante para adolescentes explorarem identidade e fé. Com louvor, debates e oficinas criativas, incentivamos a expressão pessoal fundamentada em valores cristãos.',
      'Realizamos retiros e projetos sociais que desenvolvem liderança e senso de comunidade, ajudando cada jovem a encontrar seu propósito e crescer em responsabilidade.'
    ],
    leader:       'João Maria Guedelha',
    leaderPhoto:  'src/assets/joao-maria.png',
    contact:      '+351 912 000 222',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_teens' }
    ]
  },
  {
    slug: 'jovens',
    name: 'ICMAV Jovens',
    media:   { type: 'image', src: 'src/assets/jovens.png' },
    longDescription: [
      'Os encontros de Jovens reúnem pessoas de 18 a 30 anos para momentos de adoração, estudos bíblicos e comunhão. Nosso objetivo é inspirar a geração a viver uma fé ativa no dia a dia.',
      'Além dos encontros quinzenais, promovemos seminários e missões urbanas que fortalecem a conexão com Deus e com a sociedade, capacitando cada jovem a ser luz em seu meio.'
    ],
    leader:       'Marcos Pereira',
    leaderPhoto:  'src/assets/marcos.png',
    contact:      '+351 912 000 333',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_jovens' }
    ]
  },
  {
    slug: 'homens',
    name: 'ICMAV Homens',
    media:   { type: 'image', src: 'src/assets/homens.png' },
    longDescription: [
      'O ministério de Homens oferece estudo bíblico e atividades ao ar livre, promovendo discipulado e fortalecimento de laços de amizade em Cristo.',
      'Também organizamos retiros e grupos de apoio onde os homens podem compartilhar desafios e vitórias em um ambiente de confiança e respeito mútuo.'
    ],
    leader:       'Paulo João Correia',
    leaderPhoto:  'src/assets/pj.png',
    contact:      '+351 912 000 444',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_homens' }
    ]
  },
  {
    slug: 'mulheres',
    name: 'ICMAV Mulheres',
    media:   { type: 'image', src: 'src/assets/mulheres.png' },
    longDescription: [
      'No ministério de Mulheres, cultivamos um espaço de acolhimento e crescimento espiritual através de estudos bíblicos e momentos de oração conjunta.',
      'Nossos encontros incluem workshops e eventos especiais que inspiram propósito e renovação, fortalecendo cada mulher em sua jornada de fé.'
    ],
    leader:       'Cristina Silva',
    leaderPhoto:  'src/assets/cristina.png',
    contact:      '+351 912 000 555',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_mulheres' }
    ]
  },
  {
    slug: 'casais',
    name: 'ICMAV Casais',
    media:   { type: 'image', src: 'src/assets/casais.png' },
    longDescription: [
      'O ministério de Casais promove encontros com palestras, aconselhamentos e dinâmicas que fortalecem o relacionamento conjugal à luz dos princípios bíblicos.',
      'Também organizamos conferências e retiros que oferecem ferramentas práticas para comunicação e resolução de conflitos, ajudando a construir famílias saudáveis e resilientes.'
    ],
    leader:       'Pedro Mateus',
    leaderPhoto:  'src/assets/pedro-mateus.png',
    contact:      '+351 912 000 666',
    socialMedia: [
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_casais' }
    ]
  }
]
  
  const ministry = computed(() =>
    MINISTRIES.find(m => m.slug === route.params.slug)
  )
  
  if (!ministry.value) {
    router.replace({ name: 'home' })
  }
  </script>
