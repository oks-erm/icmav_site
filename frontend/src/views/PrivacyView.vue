<!-- src/views/PrivacyView.vue -->
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
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mb-3">
          <i class="fa-solid fa-user-shield text-xs"></i>
          RGPD & Proteção de Dados
        </span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Política de Privacidade e Proteção de Dados
        </h1>
        <p class="mt-2 text-sm text-gray-400">
          Em conformidade com o Regulamento Geral sobre a Proteção de Dados (Regulamento UE 2016/679 - RGPD) e a Lei n.º 58/2019.
        </p>
      </div>

      <!-- Conteúdo Legal Estruturado -->
      <div class="space-y-8 text-sm sm:text-base text-gray-300 leading-relaxed">
        
        <!-- Secção 1 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">1.</span>
            Responsável pelo Tratamento dos Dados
          </h2>
          <p class="mb-3">
            A entidade responsável pela recolha e tratamento dos dados pessoais tratados através deste Website é a <strong>Igreja Cristã Manancial de Águas Vivas</strong> (ICMAV), com sede na Estrada de Polima N.º 609, 2785-303 São Domingos de Rana, Portugal.
          </p>
          <p>
            Para qualquer questão relacionada com a privacidade e os seus dados pessoais, pode contactar o nosso Encarregado de Proteção de Dados através do e-mail: <a href="mailto:ccicmav@gmail.com" class="text-emerald-400 hover:underline">ccicmav@gmail.com</a>.
          </p>
        </section>

        <!-- Secção 2 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">2.</span>
            Dados Pessoais Recolhidos e Finalidades
          </h2>
          <p class="mb-3">
            Tratamos apenas os dados estritamente necessários para o cumprimento das seguintes finalidades:
          </p>
          <div class="space-y-3">
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5">
              <h3 class="font-bold text-white text-sm">A. Processamento de Donativos via MB WAY e Transferência</h3>
              <p class="text-xs sm:text-sm text-gray-300 mt-1">
                <strong>Dados:</strong> Número de telemóvel (para envio do pedido de pagamento MB WAY), montante e destino do donativo.<br>
                <strong>Base Jurídica:</strong> Execução da solicitação de donativo a pedido do titular.
              </p>
            </div>
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5">
              <h3 class="font-bold text-white text-sm">B. Emissão de Recibos de Donativo para Fins Fiscais (IRS)</h3>
              <p class="text-xs sm:text-sm text-gray-300 mt-1">
                <strong>Dados:</strong> Nome completo, Número de Identificação Fiscal (NIF), Morada, Código Postal e Localidade.<br>
                <strong>Base Jurídica:</strong> Cumprimento de obrigações jurídicas e fiscais perante a Autoridade Tributária.
              </p>
            </div>
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5">
              <h3 class="font-bold text-white text-sm">C. Pedidos de Contacto e Acompanhamento Pastoral</h3>
              <p class="text-xs sm:text-sm text-gray-300 mt-1">
                <strong>Dados:</strong> Nome, e-mail, contacto telefónico e mensagem.<br>
                <strong>Base Jurídica:</strong> Consentimento do titular ao submeter o formulário de contacto.
              </p>
            </div>
          </div>
        </section>

        <!-- Secção 3 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">3.</span>
            Conservação dos Dados
          </h2>
          <p class="mb-3">
            Os dados pessoais são conservados apenas pelo período necessário para a prossecução das finalidades que motivaram a sua recolha:
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300">
            <li><strong>Dados fiscais e de faturação/recibos:</strong> Pelo prazo legal obrigatório em vigor na legislação fiscal portuguesa (10 anos).</li>
            <li><strong>Dados de processamento técnico:</strong> Apenas durante o tempo necessário para a conclusão da transação e conciliação bancária.</li>
            <li><strong>Contactos gerais:</strong> Até à conclusão do esclarecimento ou pedido solicitado.</li>
          </ul>
        </section>

        <!-- Secção 4 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">4.</span>
            Destinatários e Subcontratantes
          </h2>
          <p class="mb-3">
            A ICMAV não comercializa nem cede os seus dados pessoais a terceiros para fins de marketing ou publicidade.
          </p>
          <p class="mb-3">
            Para o estrito funcionamento do website e dos meios de pagamento, os dados podem ser transmitidos a prestadores de serviços de confiança devidamente auditados:
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300">
            <li><strong>SIBS / Instituições de Pagamento:</strong> Para o encaminhamento e liquidação do pedido MB WAY de forma encriptada.</li>
            <li><strong>Autoridade Tributária e Aduaneira (AT):</strong> Exclusivamente para efeitos de comunicação legal de donativos com benefícios fiscais.</li>
            <li><strong>Fornecedores de Infraestrutura e Alojamento Web:</strong> Sujeitos a acordos de confidencialidade e conformidade com o RGPD no espaço económico europeu.</li>
          </ul>
        </section>

        <!-- Secção 5 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">5.</span>
            Direitos do Titular dos Dados
          </h2>
          <p class="mb-3">
            Nos termos do RGPD, assistem-lhe os seguintes direitos relativos aos seus dados pessoais:
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300 mb-4">
            <li><strong>Direito de Acesso:</strong> Obter confirmação e cópia dos dados que são tratados.</li>
            <li><strong>Direito de Retificação:</strong> Solicitar a correção de dados inexatos ou incompletos.</li>
            <li><strong>Direito ao Apagamento ("Direito a ser Esquecido"):</strong> Solicitar a eliminação dos dados, desde que não colida com obrigações legais de retenção fiscal.</li>
            <li><strong>Direito à Limitação do Tratamento e Oposição:</strong> Opor-se ou restringir o tratamento em determinadas condições.</li>
            <li><strong>Direito à Portabilidade:</strong> Receber os dados num formato estruturado e de uso corrente.</li>
          </ul>
          <p>
            Para exercer qualquer um destes direitos, basta enviar uma comunicação por escrito para <a href="mailto:ccicmav@gmail.com" class="text-emerald-400 hover:underline">ccicmav@gmail.com</a>. Tem igualmente o direito de apresentar reclamação junto da autoridade de controlo nacional (Comissão Nacional de Proteção de Dados — <a href="https://www.cnpd.pt" target="_blank" rel="noopener noreferrer" class="text-emerald-400 hover:underline">www.cnpd.pt</a>).
          </p>
        </section>

        <!-- Secção 6 -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">6.</span>
            Segurança da Informação
          </h2>
          <p>
            Adotamos medidas técnicas e organizativas adequadas para proteger os dados pessoais contra perda acidental, destruição, alteração, divulgação ou acesso não autorizado, incluindo encriptação SSL/TLS em todas as comunicações eletrónicas.
          </p>
        </section>

        <!-- Secção 7: Cookies -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-emerald-400 font-mono text-lg">7.</span>
            Utilização de Cookies
          </h2>
          <p class="mb-3">
            O nosso Website utiliza cookies para garantir a segurança, navegação fluida e funcionalidades integradas.
          </p>
          <p>
            Para consultar a informação detalhada sobre os cookies utilizados, as respetivas finalidades e como geri-los, consulte a nossa <router-link to="/politica-cookies" class="text-emerald-400 font-semibold hover:underline">Política de Cookies</router-link>.
          </p>
        </section>

      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import StickyHeader from '../components/StickyHeader.vue'
import Footer from '../components/Footer.vue'
</script>
