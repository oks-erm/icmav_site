<!-- src/components/PurposeSection.vue -->
<template>
    <section id="propositos" class="py-8 bg-base-100">
      <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
  
        <!-- flex-wrap container -->
        <div class="flex flex-wrap -mx-4 justify-center">
          <div
            v-for="item in items"
            :key="item.title"
            class="w-full md:w-1/2 lg:w-1/3 px-4 mb-6"
          >
            <!-- card -->
            <div
              class="flex items-start bg-white rounded-lg shadow-md hover:shadow-lg transition h-full overflow-hidden"
            >
              <!-- icon col -->
              <div
                class="flex-shrink-0 w-20 h-full flex items-center justify-center text-2xl text-white"
                :class="`bg-${item.bg}`"
              >
                <i :class="item.icon"></i>
              </div>
  
              <!-- text col -->
              <div class="ml-4 flex flex-col justify-between p-5 h-full">
                <h3 class="text-lg font-bold mb-2">{{ item.title }}</h3>
                <p class="text-gray-600 flex-1">{{ item.desc }}</p>
  
                <!-- new verse line -->
                <p class="mt-2 text-sm italic text-gray-500">
                  {{ item.verse }}
                </p>
<!--   
                <p class="mt-4 italic text-sm text-gray-500">
                  Líder: <span class="font-medium">{{ item.leader }}</span>
                </p> -->
              </div>
            </div>
          </div>
        </div>
        <!-- /flex-wrap -->
  
      </div>
    </section>
  </template>
  
  <script setup>
  const items = [
    {
      title: 'ADORAR',
      icon: 'fas fa-sun',
      bg: 'warning',
      desc: 'Fomos criados para adorar a Deus colocando-O em primeiro lugar nas nossas vidas.',
      verse: '“Ama o Senhor, teu Deus, de todo o coração…” (Dt 6:5-6)',
      leader: 'Paulo João',
    },
    {
      title: 'PERTENCER',
      icon: 'fas fa-users',
      bg: 'primary',
      desc: 'Fomos chamados para pertencer à família de Deus, a igreja, como Seus filhos.',
      verse: '“Mas a todos quantos O receberam deu-lhes poder de serem feitos filhos de Deus.” (Jo 1:12-13)',
      leader: 'Danilo Gujral',
    },
    {
      title: 'SERVIR',
      icon: 'fas fa-hands-helping',
      bg: 'secondary',
      desc: 'Somos motivados a servir e cuidar das necessidades dos outros.',
      verse: '“Ele designou uns para apóstolos, outros para profetas… outros para servirem.” (Ef 4:11)',
      leader: 'Dina Silva',
    },
    {
      title: 'CRESCER',
      icon: 'fas fa-seedling',
      bg: 'success',
      desc: 'Somos formados para sermos semelhantes a Jesus em tudo.',
      verse: '“Sede meus imitadores, como eu o sou de Cristo.” (1 Co 11:1)',
      leader: 'Pedro Silva',
    },
    {
      title: 'ALCANÇAR',
      icon: 'fas fa-globe',
      bg: 'info',
      desc: 'Somos enviados para compartilhar esperança e vida em Jesus.',
      verse: '“Ser-me-eis testemunhas… até aos confins da terra.” (Atos 1:8)',
      leader: 'Marcelo Kutter',
    },
  ]
  </script>
  
  <style scoped>
  /* todo: nenhum CSS extra — usamos apenas Tailwind & DaisyUI */
  </style>
  