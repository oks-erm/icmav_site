<!-- src/views/MinistryDetail.vue -->
<template>
    <div class="max-w-4xl mx-auto py-16 px-4" data-aos="fade-up">
  
      <!-- Back button -->
      <button @click="$router.back()" class="btn btn-ghost mb-8">
        ← Voltar
      </button>
  
      <!-- Title -->
      <h1 class="text-4xl font-bold mb-6">{{ ministry.name }}</h1>
  
      <!-- Hero media (image/video) -->
      <div class="mb-8">
        <video
          v-if="ministry.media.type === 'video'"
          class="w-full rounded-lg shadow mb-6"
          :src="ministry.media.src"
          controls
        />
        <img
          v-else
          :src="ministry.media.src"
          alt=""
          class="w-full rounded-lg shadow mb-6"
        />
      </div>
  
      <!-- Rich description -->
      <div class="prose mb-8 text-base-content/90">
        <p v-for="(para, i) in ministry.longDescription" :key="i">
          {{ para }}
        </p>
      </div>
  
      <!-- Leader info -->
      <div class="flex items-center mb-6">
        <img
          :src="ministry.leaderPhoto"
          :alt="ministry.leader"
          class="w-24 h-24 rounded-full object-cover shadow-lg mr-4"
        />
        <div>
          <p class="font-bold text-lg">{{ ministry.leader }}</p>
          <p v-if="ministry.contact" class="text-sm">{{ ministry.contact }}</p>
        </div>
      </div>
  
      <!-- Social media links -->
      <div v-if="ministry.socialMedia.length" class="mt-6">
        <h2 class="text-xl font-semibold mb-2">Siga-nos</h2>
        <div class="flex space-x-4">
          <a
            v-for="(s, i) in ministry.socialMedia"
            :key="i"
            :href="s.link"
            target="_blank"
            class="w-10 h-10 flex items-center justify-center rounded-full bg-base-200 text-2xl text-primary hover:bg-base-300 transition"
          >
            <i :class="s.icon"></i>
          </a>
        </div>
      </div>
  
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  const MINISTRIES = [
  {
    slug: 'criancas',
    name: 'Crianças / Alfa',
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
      { icon: 'fab fa-instagram', link: 'https://instagram.com/icmav_criancas' }
    ]
  },
  {
    slug: 'teens',
    name: 'Teens',
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
    name: 'Jovens',
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
    name: 'Homens',
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
    name: 'Mulheres',
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
    name: 'Casais',
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

  
  const route = useRoute()
  const router = useRouter()
  
  // find the ministry by the slug param
  const ministry = computed(() => {
    return MINISTRIES.find((m) => m.slug === route.params.slug)
  })
  
  // if no match, redirect back to home
  if (!ministry.value) {
    router.replace({ name: 'home' })
  }
  </script>
  