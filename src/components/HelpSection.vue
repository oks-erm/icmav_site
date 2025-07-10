<!-- src/components/HelpSection.vue -->
<template>
    <section id="help" class="py-8 bg-base-100">
      <div class="max-w-7xl mx-auto px-4" data-aos="fade-up">
  
        <div class="grid grid-cols-2 gap-8">
          <!-- Pedidos de Oração -->
          <div class="bg-base-200 rounded-lg shadow-lg p-6 flex flex-col">
            <div class="flex-1">
              <h3 class="text-xl font-bold mb-2 ">Pedidos de Oração</h3>
              <p class="text-base-content/80 mb-4">
                Tem algo no coração que gostarias que a nossa comunidade levasse em oração? 
                Partilha connosco o teu pedido e iremos interceder juntos por ti.
              </p>
            </div>
            <a
              href="https://forms.gle/6k1kX1DjrECMZ8Jx8"
              target="_blank"
              class="btn btn-secondary self-start rounded-full"
              style="font-size: 100%"
            >
              Fazer Pedido de Oração
            </a>
          </div>
  
          <!-- Aconselhamento Pastoral -->
          <div class="bg-base-200 rounded-lg shadow-lg p-6 flex flex-col">
            <div class="flex-1">
              <h3 class="text-xl font-bold mb-2">Aconselhamento Pastoral</h3>
              <p class="text-base-content/80 mb-4">
                Precisas de alguém que te escute e te aconselhe biblicamente? 
                Agenda uma conversa confidencial com um dos nossos pastores.
              </p>
            </div>
            <a
              href="https://docs.google.com/forms/d/e/YOUR_COUNSEL_FORM_ID/viewform"
              target="_blank"
              class="btn btn-secondary self-start rounded-full"
              style="font-size: 100%"
            >
              Solicitar Aconselhamento
            </a>
          </div>
        </div>
      </div>
    </section>
  </template>
  