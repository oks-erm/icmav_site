<!-- src/components/HelpSection.vue -->
<template>
    <section id="help" class="py-8 bg-base-100">
      <div class="max-w-6xl mx-auto px-1 md:px-4" data-aos="fade-up">
  
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
          <!-- Pedidos de Oração -->
          <div class="bg-base-200 rounded-lg shadow-lg p-6 flex flex-col">
            <div class="flex-1">
              <h3 class="text-xl text-center sm:text-left font-bold mb-2">Pedidos de Oração</h3>
              <p class="text-base-content/80 mb-4 text-center sm:text-left">
                Podemos orar por ti? 
                Partilha connosco o teu pedido de oração.
              </p>
            </div>
            <a
              href="https://forms.gle/6k1kX1DjrECMZ8Jx8"
              target="_blank"
              class="btn btn-secondary rounded-full w-full sm:w-auto 
                mx-auto sm:mx-0 
                text-sm sm:text-base-200
                leading-snug
                whitespace-normal break-words"
              style="font-size: 100%; color: #f3e4ef;"
            >
              Fazer Pedido de Oração
            </a>
          </div>
  
          <!-- Aconselhamento Pastoral -->
          <div class="bg-base-200 rounded-lg shadow-lg p-6 flex flex-col">
            <div class="flex-1">
              <h3 class="text-xl text-center sm:text-left font-bold mb-2">Aconselhamento Pastoral</h3>
              <p class="text-base-content/80 mb-4 text-center sm:text-left">
                Precisas de ser ouvido/a e que alguém te aconselhe? 
                Agenda uma conversa privada com alguém da nossa equipa pastoral.
              </p>
            </div>
            <a
              href="https://forms.gle/PtJSnsfxNU9pQvez9"
              target="_blank"
              class="btn btn-secondary rounded-full w-full sm:w-auto 
                mx-auto sm:mx-0 
                text-sm sm:text-base 
                leading-snug
                whitespace-normal break-words"
              style="font-size: 100%; color: #f3e4ef;"
            >
              Solicitar Aconselhamento pastoral
            </a>
          </div>
        </div>
      </div>
    </section>
  </template>
  