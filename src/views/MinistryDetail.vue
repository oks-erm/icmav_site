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
    media: { type: 'image', src: '/assets/teens.png' },
    longDescription: [
      'Um espaço vibrante para adolescentes explorarem perguntas de fé e identidade. Música, debates e eventos criativos fazem parte de cada encontro.',
      'Nosso objetivo é formar líderes sólidos e relacionamentos saudáveis nesta fase tão importante da vida.'
    ],
    leader: 'João Maria Guedelha',
    leaderPhoto: '/assets/joao-maria.jpg',
    contact: '+351 912 000 222',
    instagram: 'https://instagram.com/icmav_teens'
  },
  {
    slug: 'jovens',
    name: 'Jovens',
    media: { type: 'image', src: '/assets/jovens.jpg' },
    longDescription: [
      'Encontros quinzenais para jovens de 18 a 30 anos, com louvor, texto bíblico e muita interação. Queremos inspirar você a viver com propósito e fé autêntica.',
      'Retiro anual, grupos de discipulado e projetos sociais fazem parte da nossa jornada de crescimento.'
    ],
    leader: 'Marcos Pereira',
    leaderPhoto: '/assets/marcos-pereira.jpg',
    contact: '+351 912 000 333',
    instagram: 'https://instagram.com/icmav_jovens'
  },
  {
    slug: 'homens',
    name: 'Homens',
    media: { type: 'image', src: '/assets/homens.jpg' },
    longDescription: [
      'Ministério de homens focado em discipulado, companheirismo e responsabilidade. Encontros mensais com estudo bíblico e atividades ao ar livre.',
      'Aqui você encontrará suporte para a sua caminhada espiritual e amizades sólidas para a vida inteira.'
    ],
    leader: 'Paulo João Correia',
    leaderPhoto: '/assets/paulo-joao.jpg',
    contact: '+351 912 000 444',
    instagram: 'https://instagram.com/icmav_homens'
  },
  {
    slug: 'mulheres',
    name: 'Mulheres',
    media: { type: 'image', src: '/assets/mulheres.jpg' },
    longDescription: [
      'Espaço de acolhimento e fortalecimento para mulheres de todas as idades. Nossos encontros incluem estudo bíblico, orações em grupo e eventos especiais.',
      'Nossa missão é caminhar lado a lado, encorajando cada mulher a descobrir seu valor em Cristo.'
    ],
    leader: 'Cristina Silva',
    leaderPhoto: '/assets/cristina-silva.jpg',
    contact: '+351 912 000 555',
    instagram: 'https://instagram.com/icmav_mulheres'
  },
  {
    slug: 'casais',
    name: 'Casais',
    media: { type: 'image', src: '/assets/casais.jpg' },
    longDescription: [
      'Para casais que desejam fortalecer o relacionamento à luz do evangelho. Palestras, aconselhamentos e convivências promovem comunicação e intimidade saudável.',
      'Nosso objetivo é ver famílias transformadas pela graça e pelo amor que aprendemos em Jesus.'
    ],
    leader: 'Pedro Mateus',
    leaderPhoto: '/assets/pedro-mateus.jpg',
    contact: '+351 912 000 666',
    instagram: 'https://instagram.com/icmav_casais'
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
  