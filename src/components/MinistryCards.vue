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
        description: 'Um grupo de mulheres que merece um espaço onde é ouvida, valorizada e encorajada.',

    },
    {
        name: 'Homens',
        slug: 'homens',
        icon: 'fas fa-hands-helping',
        bg: 'warning',
        description: 'Grupo de camaradagem, troca e crescimento para todas as fases da vida .',
    },
    {
        name: 'Casais',
        slug: 'casais',
        icon: 'fas fa-globe',
        bg: 'error',
        description: 'Porque cuidar do relacionamento a dois também é uma forma de amar.',
    },
    {
        name: 'Jovens',
        slug: 'jovens',
        icon: 'fas fa-heart',
        bg: 'secondary',
        description: 'Bora lá viver que vai além do comum, com propósito e significado.',
    },
    {
        name: 'Teens',
        slug: 'teens',
        icon: 'fas fa-music',
        bg: 'primary',
        description: 'Aqui é onde começa a tua jornada: com gente real e fé prática.',
    },
    {
        name: 'Crianças',
        slug: 'criancas',
        icon: 'fas fa-hands-holding-child',
        bg: 'accent',
        description: 'Aqui a imaginação voa e o coração aprende o que realmente importa.',
    }
]
</script>
  
