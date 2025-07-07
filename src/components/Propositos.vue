<!-- src/components/PurposeSection.vue -->
<template>
    <section id="propositos" class="py-8 bg-base-100">
      <div class="max-w-6xl mx-auto px-4" data-aos="fade-up">
  
        <!-- flex-wrap container with negative margins -->
        <div class="flex flex-wrap -mx-4 flex justify-center">
          <div
            v-for="item in items"
            :key="item.title"
            class="s:w-full md:w-1/2 lg:w-1/3 px-4 mb-6"
          >
            <!-- card -->
            <div class="flex items-start bg-white rounded-lg shadow-md hover:shadow-lg transition h-full overflow-hidden" style="align-items: center;">
              <!-- icon col -->
              <div
                class="flex-shrink-0 w-20 h-full flex items-center justify-center text-2xl text-white"
                :class="`bg-${item.bg}`"
              >
                <i :class="item.icon"></i>
              </div>
              <!-- text col -->
              <div class="ml-4 flex-1 flex flex-col p-4">
                <h3 class="text-lg font-bold mb-2">{{ item.title }}</h3>
                <p class="text-gray-600 flex-1">{{ item.desc }}</p>
                <p class="mt-4 italic text-sm text-gray-500">
                  Líder: <span class="font-medium">{{ item.leader }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
        <!-- /flex-wrap container -->
  
      </div>
    </section>
  </template>
  
  <script setup>
  const items = [
    {
      title: 'ADORAR',
      icon: 'fas fa-sun',
      bg:'yellow-300',
      desc: 'Adorar a Deus é celebrar quem Ele é com todo o nosso coração.',
      leader: 'Paulo João',
    },
    {
      title: 'PERTENCER',
      icon: 'fas fa-users',
      bg: 'primary',
      desc: 'Aqui encontras um lugar de amizade e acolhimento.',
      leader: 'Danilo Gujral',
    },
    {
      title: 'CRESCER',
      icon: 'fas fa-seedling',
      bg: 'green-500', 
      desc: 'Juntos, aprendemos o que Jesus nos ensinou e colocamos em prática no dia a dia.',
      leader: 'Pedro Silva',
    },
    {
      title: 'SERVIR',
      icon: 'fas fa-hands-helping',
      bg:  'secondary',
      desc: 'Colocamos mãos à obra para cuidar de quem precisa ao nosso redor.',
      leader: 'Dina Silva',
    },
    {
      title: 'ALCANÇAR',
      icon: 'fas fa-globe',
      bg: 'info',
      desc: 'Somos enviados para compartilhar esperança e vida em Jesus.',
      leader: 'Marcelo Kutter',
    },
  ]
  </script>
  
  <style scoped>
  /* no extra CSS needed; gutters, wrapping and equal heights now match your Ministérios setup */
  </style>
  