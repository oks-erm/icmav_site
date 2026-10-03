<!-- src/views/TermsView.vue -->
<template>
  <div class="min-h-screen flex flex-col bg-gray-950 text-gray-100">
    <StickyHeader />

    <main class="flex-grow py-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
      <!-- Breadcrumb & Voltar -->
      <div class="mb-8">
        <router-link
          to="/"
          class="inline-flex items-center gap-2 text-xs font-semibold text-gray-400 hover:text-white transition-colors cursor-pointer group"
        >
          <i class="fa-solid fa-arrow-left text-xs group-hover:-translate-x-1 transition-transform"></i>
          <span>Voltar ao Início</span>
        </router-link>
      </div>

      <!-- Título & Cabeçalho -->
      <div class="mb-10 pb-6 border-b border-white/10">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-primary/20 text-primary border border-primary/30 mb-3">
          <i class="fa-solid fa-scale-balanced text-xs"></i>
          Conformidade Legal
        </span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Termos e Condições de Utilização
        </h1>
        <p class="mt-2 text-sm text-gray-400">
          Última atualização: Março de 2025 • Em vigor para a Igreja Cristã Manancial de Águas Vivas (ICMAV)
        </p>
      </div>

      <!-- Conteúdo Legal Estruturado -->
      <div class="space-y-8 text-sm sm:text-base text-gray-300 leading-relaxed">
        
        <!-- Secção 1 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">1.</span>
            Identificação da Entidade Titular
          </h2>
          <p class="mb-3">
            O presente sítio web (doravante designado por "Website") é propriedade e gerido pela <strong>Igreja Cristã Manancial de Águas Vivas</strong> (doravante "ICMAV"), pessoa coletiva religiosa sem fins lucrativos.
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300">
            <li><strong>Denominação:</strong> Igreja Cristã Manancial de Águas Vivas (ICMAV)</li>
            <li><strong>Sede / Morada:</strong> Estrada de Polima N.º 609, 2785-303 São Domingos de Rana, Portugal</li>
            <li><strong>E-mail de Contacto:</strong> <a href="mailto:ccicmav@gmail.com" class="text-primary hover:underline">ccicmav@gmail.com</a></li>
            <li><strong>E-mail de Tesouraria:</strong> <a href="mailto:tesouraria.icmav@gmail.com" class="text-primary hover:underline">tesouraria.icmav@gmail.com</a></li>
            <li><strong>Telefone:</strong> +351 934 693 310</li>
          </ul>
        </section>

        <!-- Secção 2 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">2.</span>
            Objeto e Âmbito de Aplicação
          </h2>
          <p class="mb-3">
            Os presentes Termos e Condições regulam o acesso, navegação e utilização do Website da ICMAV, bem como o processo de realização de contribuições voluntárias, donativos, dízimos e ofertas por via eletrónica.
          </p>
          <p>
            Ao aceder ao Website e ao utilizar as suas funcionalidades, o utilizador declara ter lido, compreendido e aceite integralmente estes Termos e Condições, bem como a respetiva <router-link to="/politica-privacidade" class="text-primary hover:underline font-semibold">Política de Privacidade</router-link>.
          </p>
        </section>

        <!-- Secção 3 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">3.</span>
            Natureza dos Donativos e Contribuições
          </h2>
          <p class="mb-3">
            Todas as transações efetuadas através do módulo de contribuições têm a natureza de <strong>donativos voluntários</strong> e de apoio à atividade religiosa, social, cultural e missionária desenvolvida pela ICMAV.
          </p>
          <p class="mb-3">
            Os donativos são expressos em <strong>Euros (€ / EUR)</strong>. Não constituem contraprestação direta pela aquisição de bens comerciais ou serviços sujeitos a IVA de natureza comercial, enquadrando-se na isenção prevista no Código do IVA para atividades religiosas/sociais de entidades sem fins lucrativos.
          </p>
          <p>
            O utilizador pode selecionar a destinação pretendida para a sua contribuição (ex.: Ofertas Gerais, Dízimos, Missões, Obras e Projetos Especiais), sendo o valor integralmente afeto aos fins estatutários da instituição.
          </p>
        </section>

        <!-- Secção 4 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">4.</span>
            Métodos de Pagamento e Segurança
          </h2>
          <p class="mb-3">
            O Website disponibiliza meios eletrónicos seguros de pagamento autorizados em Portugal:
          </p>
          <ul class="space-y-2 pl-4 list-disc mb-3">
            <li>
              <strong>MB WAY:</strong> O processamento é efetuado através de canais seguros em articulação com a rede SIBS. O utilizador deve autorizar o débito diretamente na aplicação MB WAY instalada no seu dispositivo móvel no prazo limite de validade do pedido (habitualmente 4 minutos).
            </li>
            <li>
              <strong>Transferência Bancária (SEPA):</strong> Disponibilização de IBAN oficial e dados da conta bancária institucional titulada pela ICMAV no NOVO BANCO, SA.
            </li>
          </ul>
          <p>
            A ICMAV não armazena nem tem acesso a credenciais bancárias privadas, PINs ou números de cartões dos utilizadores. Todas as transmissões de dados são cifradas através de protocolo seguro <strong>HTTPS (SSL/TLS)</strong>.
          </p>
        </section>

        <!-- Secção 5 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">5.</span>
            Emissão de Recibos e Efeitos Fiscais
          </h2>
          <p class="mb-3">
            O doador que pretenda a emissão de recibo para efeitos fiscais (IRS) deve assinalar essa opção no formulário de contribuição ou remeter o comprovativo para a Tesouraria da ICMAV (<a href="mailto:tesouraria.icmav@gmail.com" class="text-primary hover:underline">tesouraria.icmav@gmail.com</a>), facultando o seu Nome Completo, NIF e Morada.
          </p>
          <p>
            Os recibos de donativo são emitidos em conformidade com a legislação fiscal portuguesa e o Estatuto dos Benefícios Fiscais aplicável.
          </p>
        </section>

        <!-- Secção 6 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">6.</span>
            Política de Cancelamento e Reembolsos
          </h2>
          <p>
            As condições aplicáveis a retificações de montantes, duplicidade de pagamentos por erro ou pedidos de esclarecimento encontram-se descritas detalhadamente na nossa <router-link to="/politica-cancelamento-reembolso" class="text-primary hover:underline font-semibold">Política de Cancelamento e Reembolsos</router-link>.
          </p>
        </section>

        <!-- Secção 7 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-primary font-mono text-lg">7.</span>
            Lei Aplicável e Foro Competente
          </h2>
          <p class="mb-3">
            Os presentes Termos e Condições regem-se pela lei portuguesa.
          </p>
          <p>
            Para a resolução de qualquer litígio emergente da interpretação ou execução dos presentes Termos, é competente o Tribunal da Comarca de Cascais / Lisboa Oeste, com expressa renúncia a qualquer outro.
          </p>
        </section>

      </div>

      <!-- Caixa de Suporte / Contacto -->
      <div class="mt-10 p-6 bg-primary/10 border border-primary/20 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 class="text-base font-bold text-white">Dúvidas sobre os nossos termos?</h3>
          <p class="text-xs sm:text-sm text-gray-300">A nossa equipa de apoio e tesouraria está disponível para esclarecer qualquer questão.</p>
        </div>
        <a
          href="mailto:ccicmav@gmail.com"
          class="px-5 py-2.5 rounded-xl bg-primary text-white font-semibold text-xs sm:text-sm shadow-md hover:bg-primary/90 transition-all cursor-pointer whitespace-nowrap"
        >
          Contactar ICMAV
        </a>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import StickyHeader from '../components/StickyHeader.vue'
import Footer from '../components/Footer.vue'
</script>
