<!-- src/components/Pastores.vue -->
<template>
    <div>
        <!-- ============================= -->
        <!-- 1) SCROLLABLE ROW OF PASTORES -->
        <!-- ============================= -->
        <div class="relative">
            <!-- We’re still using overflow-x-auto to allow horizontal scrolling -->
            <!-- You can preserve your hide-scrollbar utility so the native scrollbar is hidden -->
            <div ref="scrollContainer"
                class="overflow-x-auto scroll-smooth px-8 hide-scrollbar py-6"
                @scroll="checkArrows">
                <div class="flex justify-center">
                <div
                    v-for="(p,i) in pastors" :key="p.id"
                    @click="toggleBio(p.id)"
                    class="flex-shrink-0 w-36 flex flex-col items-center cursor-pointer transition-transform hover:scale-105"
                    :style="{
                    marginRight: (pastors[i+1] && pastors[i+1].id === p.spouseId)
                        ? '-0.8rem'
                        : '2.5rem'
                    }"
                    :data-aos="'fade-up'"
                    :data-aos-delay="i * 100"
                >
                    <div class="w-36 h-36 rounded-full overflow-hidden shadow-lg">
                    <img :src="p.photo" :alt="p.name" class="object-cover w-full h-full" />
                    </div>
                    <p class="mt-2 text-center font-medium">{{ p.name }}</p>
                </div>
                </div>
            </div>

            <!-- OPTIONAL: Left/Right arrow indicators -->
            <!-- Un‐comment and adjust if you want manual arrow buttons -->

            <button v-if="showLeftArrow"
                class="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 hover:bg-white z-10"
                @click="scrollLeft">
                <i class="fas fa-chevron-left text-xl text-gray-700"></i>
            </button>
            <button v-if="showRightArrow"
                class="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 hover:bg-white z-10"
                @click="scrollRight">
                <i class="fas fa-chevron-right text-xl text-gray-700"></i>
            </button>

        </div>

        <!-- ============================= -->
        <!-- 2) DROP‐DOWN BIO AREA -->
        <!-- ============================= -->
        <transition name="slide-fade">
            <div v-if="activePastor" class="mt-8 px-4">
                <div class="bg-base-100 rounded-lg shadow-lg p-6 text-base-content/90 leading-relaxed"
                    data-aos="fade-up">
                    <!-- 1) Pastor’s name on top -->
                    <h3 class="text-2xl px-36 font-bold mb-4">{{ activePastor.name }}</h3>

                    <!-- 2) Floating circle photo -->
                    <img :src="activePastor.photo" :alt="activePastor.name"
                        class="w-32 h-32 rounded-full object-cover float-left mr-4 mb-4 shadow-md" />

                    <!-- 3) Long bio copy that wraps around the floated image -->
                    <p>
                        {{ activePastor.bio }}
                    </p>
                </div>
            </div>

        </transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'


const pastors = [
    {
        id: 1,
        name: 'Pr Henrique Pereira',
        photo: '/src/assets/h.png',
        bio:
            'Pr. João ministra ao público infantil há mais de 8 anos, criando programas lúdicos e reflexivos que ajudam as crianças a conhecerem mais de Jesus de forma criativa.',
        spouseId: 2,
    },
    {
        id: 2,
        name: 'Pra Minita Pereira',
        photo: '/src/assets/minita.png',
        bio:
            'Pra. Minita é a líder do ministério de jovens, organizando retiros e encontros semanais. Seu objetivo é inspirar a próxima geração a viver com propósito e fé.',
        spouseId: 1,
    },

    {
        id: 3,
        name: 'Pr Rogério Trindade',
        photo: '/src/assets/rog.png',
        bio:
            'Pr. RR atua no ministério de família, auxiliando novos casais e desenvolvendo estudos de apoio a jovens. Acredita na força da comunidade unida em fé.',
        spouseId: 4,
    },
    {
        id: 4,
        name: 'Pra Johana Villarroel',
        photo: '/src/assets/johana.png',
        bio:
            'Pr. João ministra ao público infantil há mais de 8 anos, criando programas lúdicos e reflexivos que ajudam as crianças a conhecerem mais de Jesus de forma criativa.',
        spouseId: 3,
    },
    {
        id: 5,
        name: 'Pr Manza Garcia',
        photo: '/src/assets/manza.png',
        bio:
            'Pr. Maria lidera o ministério feminino e periodicidade de estudos bíblicos para mulheres de todas as idades. Seu foco é empoderar mulheres para viverem seu propósito.',
    },
    {
        id: 6,
        name: 'Pr Danilo Gujral',
        photo: '/src/assets/danilo.png',
        bio:
            'Pr. Pedro coordena projetos sociais, cuidando de comunidades locais e missionárias. Tem um coração para levar esperança e ajuda prática àqueles que precisam.',
        spouseId: 7,
    },
    {
        id: 7,
        name: 'Pra Havani Gujral',
        photo: '/src/assets/havani.png',
        bio:
            'Pr. João ministra ao público infantil há mais de 8 anos, criando programas lúdicos e reflexivos que ajudam as crianças a conhecerem mais de Jesus de forma criativa.',
        spouseId: 6,
    },
    {
        id: 8,
        name: 'Pr Paulo João Correia',
        photo: '/src/assets/pj.png',
        bio:
            "Pr. Paulo é o pastor sênior da igreja, liderando a visão geral e a direção espiritual. Com mais de 20 anos de ministério, ele é um mentor para muitos.",
        spouseId: 9,
    },
    {
        id: 9,
        name: 'Pra Denise Correia',
        photo: '/src/assets/denise.png',
        bio:
            'Pr. João ministra ao público infantil há mais de 8 anos, criando programas lúdicos e reflexivos que ajudam as crianças a conhecerem mais de Jesus de forma criativa.',
        spouseId: 8,
    }
]

//
// 2) ACTIVE ID STATE + COMPUTED PASTOR
//
const activeId = ref(null)

// Toggle logic: if you click the same pastor again, collapse. Otherwise open the clicked one.
function toggleBio(id) {
    activeId.value = activeId.value === id ? null : id
}

const activePastor = computed(() =>
    pastors.find((p) => p.id === activeId.value)
)

//
// 3) OPTIONAL SCROLL‐ARROW LOGIC
//    (Only if you uncomment the arrow buttons above)
//
// - showLeftArrow/showRightArrow booleans check if scroll is at extremes.
// - scrollLeft/scrollRight animate the scrollContainer.
//
// If you do not need arrow buttons, you can remove everything from here to “onMounted”.
//
const scrollContainer = ref(null)
const showLeftArrow = ref(false)
const showRightArrow = ref(false)

function checkArrows() {
    const el = scrollContainer.value
    if (!el) return
    showLeftArrow.value = el.scrollLeft > 10
    showRightArrow.value = el.scrollLeft + el.clientWidth + 10 < el.scrollWidth
}

function scrollLeft() {
    const el = scrollContainer.value
    if (!el) return
    el.scrollBy({ left: -200, behavior: 'smooth' })
}

function scrollRight() {
    const el = scrollContainer.value
    if (!el) return
    el.scrollBy({ left: +200, behavior: 'smooth' })
}

// Watch scroll position on mount in case content overflows immediately
onMounted(() => {
    checkArrows()
})
</script>

<style scoped>
/* =================================================
     1) HIDE NATIVE SCROLLBAR (chromium + firefox)
     ================================================= */
.hide-scrollbar {
    scrollbar-width: none;
    /* Firefox */
}

.hide-scrollbar::-webkit-scrollbar {
    display: none;
    /* Chrome/Safari */
}

/* =================================================
     2) SLIDE + FADE TRANSITION FOR BIO PANEL
     ================================================= */
.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.slide-fade-enter-to,
.slide-fade-leave-from {
    opacity: 1;
    transform: translateY(0);
}
</style>
  
