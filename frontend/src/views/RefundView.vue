<!-- src/views/RefundView.vue -->
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
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 mb-3">
          <i class="fa-solid fa-rotate-left text-xs"></i>
          Transparência & Garantias
        </span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Política de Cancelamento e Reembolsos
        </h1>
        <p class="mt-2 text-sm text-gray-400">
          Procedimentos para regularização de transações, erros de processamento e cancelamento de pagamentos.
        </p>
      </div>

      <!-- Conteúdo Legal Estruturado -->
      <div class="space-y-8 text-sm sm:text-base text-gray-300 leading-relaxed">
        
        <!-- Secção 1 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-indigo-400 font-mono text-lg">1.</span>
            Enquadramento dos Donativos
          </h2>
          <p class="mb-3">
            As contribuições, dízimos e ofertas efetuados através do sítio web da <strong>Igreja Cristã Manancial de Águas Vivas (ICMAV)</strong> constituem doações voluntárias e a título gratuito, destinadas exclusivamente à prossecução da missão espiritual, social e comunitária da instituição.
          </p>
          <p>
            Por se tratarem de liberalidades e donativos sem contraprestação de bens materiais comerciais, os donativos consumados não se encontram sujeitos ao direito de livre resolução aplicável a contratos de compra e venda mercantil, sem prejuízo das salvaguardas por erro ou anomalia operacional expressas no ponto seguinte.
          </p>
        </section>

        <!-- Secção 2 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-indigo-400 font-mono text-lg">2.</span>
            Situações de Devolução e Retificação de Valores
          </h2>
          <p class="mb-3">
            A ICMAV compromete-se a analisar e proceder à restituição integral ou parcial dos valores nas seguintes circunstâncias:
          </p>
          <ul class="space-y-2 pl-4 list-disc text-gray-300">
            <li>
              <strong>Erro no Montante Introduzido:</strong> Sempre que o utilizador introduzir por lapso manifesto um valor incorreto (por exemplo, erro de vírgula ou dígitos adicionais).
            </li>
            <li>
              <strong>Duplicação de Transação:</strong> Quando, por anomalia de rede ou repetição involuntária de operação, ocorrer débito duplo do mesmo montante.
            </li>
            <li>
              <strong>Operação Não Autorizada ou Fraudulenta:</strong> Comprovada a utilização abusiva do meio de pagamento sem conhecimento ou consentimento do seu legítimo titular.
            </li>
          </ul>
        </section>

        <!-- Secção 3 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-indigo-400 font-mono text-lg">3.</span>
            Prazo e Procedimento para Solicitação
          </h2>
          <p class="mb-3">
            Para solicitar a verificação e eventual reembolso de uma contribuição, o titular deve comunicar a situação à Tesouraria da ICMAV no prazo máximo de <strong>14 (catorze) dias de calendário</strong> após a data do débito.
          </p>
          <p class="mb-3">
            O pedido deve ser remetido para o endereço eletrónico <a href="mailto:tesouraria.icmav@gmail.com" class="text-indigo-400 hover:underline font-bold">tesouraria.icmav@gmail.com</a>, indicando:
          </p>
          <ul class="space-y-1 pl-4 list-disc text-gray-300 mb-3">
            <li>Nome completo e contacto telefónico;</li>
            <li>Data e hora aproximada da operação;</li>
            <li>Montante debitado;</li>
            <li>Comprovativo da transação (notificação MB WAY ou extrato bancário com referência da operação);</li>
            <li>IBAN para o qual deve ser processada a devolução.</li>
          </ul>
        </section>

        <!-- Secção 4 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-indigo-400 font-mono text-lg">4.</span>
            Processamento e Meio de Reembolso
          </h2>
          <p class="mb-3">
            Após validação da ocorrência pela equipa de tesouraria, o reembolso será processado no prazo máximo de <strong>5 a 10 dias úteis</strong>.
          </p>
          <p>
            O reembolso é realizado, preferencialmente, pelo mesmo método utilizado no pagamento ou por transferência bancária direta para o IBAN indicado pelo titular, sem cobrança de taxas adicionais imputáveis ao doador pelo processamento da devolução.
          </p>
        </section>

        <!-- Secção 5 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-indigo-400 font-mono text-lg">5.</span>
            Cancelamento de Pedidos Pendentes (MB WAY)
          </h2>
          <p class="mb-3">
            No caso de pagamentos solicitados através do método <strong>MB WAY</strong>, se o utilizador não validar o pedido na respetiva aplicação móvel dentro do tempo limite estabelecido pelo sistema (cerca de 4 minutos), a operação expira de forma automática e imediata, sem qualquer encargo ou débito na sua conta bancária.
          </p>
        </section>

      </div>

      <!-- Caixa de Contacto -->
      <div class="mt-10 p-6 bg-gray-900 border border-white/10 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 class="text-base font-bold text-white">Necessita de apoio com uma contribuição?</h3>
          <p class="text-xs sm:text-sm text-gray-400">A nossa equipa de tesouraria está ao seu dispor para esclarecer qualquer situação.</p>
        </div>
        <a
          href="mailto:tesouraria.icmav@gmail.com"
          class="px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs sm:text-sm shadow-md hover:bg-indigo-500 transition-all cursor-pointer whitespace-nowrap"
        >
          Contactar Tesouraria
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
