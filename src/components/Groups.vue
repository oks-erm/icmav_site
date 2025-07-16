<template>
    <div class="max-w-3xl mx-auto px-4 space-y-6" data-aos="fade-up">
        <!-- Intro copy -->
        <div class="space-y-4 text-base leading-relaxed text-center">

            <blockquote class="italic text-center border-l-4 border-info pl-4">
                “Uma comunidade saudável é ser grande e pequena ao mesmo tempo".<br />
                <span class="font-medium">— Rick Warren</span>
            </blockquote>

            <p>
                Acreditamos que relacionamentos confiáveis e seguros tornam-se fundamentais
                para um novo projeto de vida. Num inquérito que fizemos em 2011, na ICMAV e fora dela, às pessoas da
                comunidade,
                essa foi a conclusão mais forte a que chegamos. Deus tem uma família, e quer que tu também pertenças a
                ela. Os PGs são uma
                forma de experimentarmos Deus e uma nova vida em família. Encontros semanais, quinzenais ou mensais
                em pequenos grupos de interesse ou outros,
                para as várias camadas etárias. Consulte a lista de Grupos, localidades e
                características dos mesmos.
            </p>
        </div>

        <!-- Join Button -->
        <div class="flex justify-center mt-20" data-aos="fade-up" data-aos-delay="200">
            <button @click="scrollTo('ministerios')" id="join" class="btn btn-info rounded-full btn-xl py-4 px-12">
                Junte-se a um Pequeno Grupo
            </button>
        </div>
    </div>
</template>

<script setup>
// Local data; you could also import from a separate file or props
const groups = [
    { city: 'Lisboa', schedule: 'Terças 19h', mapLink: 'https://goo.gl/maps/…' },
    { city: 'Porto', schedule: 'Quartas 20h', mapLink: 'https://goo.gl/maps/…' },
    { city: 'Coimbra', schedule: 'Sextas 18h', mapLink: 'https://goo.gl/maps/…' },
]
</script>

<style scoped>
/* scoped styles if needed */
</style>
  
