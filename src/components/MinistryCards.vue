<template>
    <section id="ministerios" class="py-12 bg-base-100">
        <div class="max-w-7xl mx-auto px-4">
            <!-- FLEX WRAP CONTAINER -->
            <div class="flex flex-wrap -mx-4" data-aos="fade-up" data-aos-delay="200">
                <!-- EACH MINISTRY CARD -->
                <div v-for="m in ministries" :key="m.slug" class=" md:w-1/2 lg:w-1/3 px-4 mb-6">
                    <router-link :to="{ name: 'MinistryDetail', params: { slug: m.slug } }"
                        class="flex items-start space-x-4 bg-base-100 rounded-lg shadow-lg hover:shadow-2xl transition p-6 h-full">
                        <!-- ICON CIRCLE -->
                        <div class="flex-shrink-0 w-14 h-14 flex items-center justify-center rounded-full text-3xl text-white"
                            :class="`bg-${m.bg}`">
                            <i :class="`${m.icon} fa-fw`"></i>
                        </div>

                        <!-- TITLE & DESCRIPTION -->
                        <div class="flex-1">
                            <h3 class="text-xl font-bold mb-1">{{ m.name }}</h3>
                            <p class="text-sm text-base-content/70">
                                {{ m.description }}
                            </p>
                        </div>
                    </router-link>
                </div>
                <!-- /END EACH CARD -->
            </div>
            <!-- /END FLEX WRAP CONTAINER -->
        </div>
    </section>
</template>

<script setup>
const ministries = [
    {
        name: 'Mulheres',
        slug: 'mulheres',
        icon: 'fas fa-female',
        bg: 'info',
        description: 'Grupo de apoio e estudo bíblico para mulheres. Encontros quinzenais para debates e crescimento.',
    },
    {
        name: 'Homens',
        slug: 'homens',
        icon: 'fas fa-hands-helping',
        bg: 'warning',
        description: 'Encontros de discipulado e comunhão masculina. Encontros quinzenais para debates e crescimento.',
    },
    {
        name: 'Casais',
        slug: 'casais',
        icon: 'fas fa-globe',
        bg: 'error',
        description: 'Projetos sociais e missões para impactar nossa comunidade.',
    },
    {
        name: 'Jovens',
        slug: 'jovens',
        icon: 'fas fa-heart',
        bg: 'secondary',
        description: 'Encontros quinzenais para juventude, debates e crescimento. Encontros quinzenais para juventude, debates e crescimento.',
    },
    {
        name: 'Teens',
        slug: 'teens',
        icon: 'fas fa-music',
        bg: 'primary',
        description: 'Culto de louvor e adoração, com música e reflexão bíblica. Culto de louvor e adoração, com música e reflexão bíblica.',
    },
    {
        name: 'Crianças',
        slug: 'criancas',
        icon: 'fas fa-hands-holding-child',
        bg: 'accent',
        description: 'Programa infantil com atividades lúdicas, ensinamentos e louvor.',
    }
]
</script>
  
