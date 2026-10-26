<!-- src/views/DonationFormView.vue -->

<template>
  <div class="min-h-screen bg-slate-950 text-gray-100 flex flex-col justify-between relative overflow-hidden selection:bg-primary selection:text-white">
    
    <!-- Efeitos de Luz e Gradiente de Fundo (Atmosphere) -->
    <div
      class="pointer-events-none absolute inset-0 z-0"
      style="background: radial-gradient(360px circle at 50% 100px, rgba(14, 165, 233, 0.16), transparent 75%), radial-gradient(280px circle at 85% 90%, rgba(99, 102, 241, 0.12), transparent 75%);"
    ></div>

    <!-- ══════════════════ TOPO / NAVEGAÇÃO ══════════════════ -->
    <header class="relative z-10 w-full max-w-4xl mx-auto px-4 pt-6 sm:pt-8 flex items-center justify-between">
      <router-link
        to="/"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs sm:text-sm font-semibold text-gray-300 bg-white/5 hover:bg-white/10 hover:text-white transition-all border border-white/10 cursor-pointer group"
      >
        <svg class="w-3 h-3 fill-current group-hover:-translate-x-1 transition-transform" viewBox="0 0 448 512" aria-hidden="true"><path d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/></svg>
        <span>Voltar ao site</span>
      </router-link>

      <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        Ambiente Seguro SSL/TLS
      </span>
    </header>

    <!-- ══════════════════ CONTEÚDO PRINCIPAL (MOBILE FIRST) ══════════════════ -->
    <main class="relative z-10 w-full max-w-lg mx-auto px-4 py-4 sm:py-6 flex flex-col items-center">
      
      <!-- CONTAINER TOPO: LOGO GRANDE EM MARCA DE ÁGUA + TÍTULOS -->
      <div class="relative w-full flex flex-col items-center text-center">
        
        <!-- Logótipo puxado ~5% para cima com 50% de transparência -->
        <div class="absolute -top-3 sm:-top-4 md:-top-5 left-1/2 -translate-x-1/2 w-64 sm:w-80 md:w-96 pointer-events-none z-0">
          <img
            :src="logoWhite"
            alt="ICMAV Logo"
            fetchpriority="high" decoding="async" class="w-full h-auto object-contain opacity-50"
          />
        </div>

        <!-- Títulos posicionados do meio para baixo do logótipo com espaçamento equilibrado -->
        <div class="relative z-10 pt-24 sm:pt-32 pb-3.5 sm:pb-4 space-y-1.5">
          <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight" style="text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);">
            Contribuição & Generosidade
          </h1>
          <p class="text-xs sm:text-sm text-gray-200 max-w-xs mx-auto font-medium" style="text-shadow: 0 2px 6px rgba(0, 0, 0, 0.95);">
            Apoia a missão, os projetos e a comunidade da ICMAV.
          </p>
        </div>
      </div>

      <!-- ══════════════════ CARTÃO DO FORMULÁRIO ══════════════════ -->
      <div class="relative z-20 mt-0 sm:mt-0.5 w-full bg-white text-gray-900 rounded-3xl shadow-2xl border border-gray-100 p-5 sm:p-8 transition-all">
        
        <!-- 1. SELETOR DE MODO DE PAGAMENTO (TABS MODERNAS) -->
        <div v-if="!mbwayStatus && !loading" class="mb-5">
          <div class="grid grid-cols-2 p-1 bg-gray-100/90 rounded-2xl gap-1">
            <button
              type="button"
              @click="paymentMethod = 'mbway'"
              class="flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl font-bold text-xs sm:text-sm transition-all cursor-pointer"
              :class="[
                paymentMethod === 'mbway'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-900'
              ]"
            >
              <MbwayLogo height="18px" />
            </button>

            <button
              type="button"
              @click="paymentMethod = 'bank_transfer'"
              class="flex items-center justify-center gap-2 py-2.5 px-3 rounded-xl font-bold text-xs sm:text-sm transition-all cursor-pointer"
              :class="[
                paymentMethod === 'bank_transfer'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-900'
              ]"
            >
              <svg class="w-3.5 h-3.5 fill-current text-primary" viewBox="0 0 512 512" aria-hidden="true"><path d="M243.4 2.6l-224 96c-14 6-21.8 21-18.7 35.8S16.8 160 32 160l0 8c0 13.3 10.7 24 24 24l400 0c13.3 0 24-10.7 24-24l0-8c15.2 0 28.3-10.7 31.3-25.6s-4.8-29.9-18.7-35.8l-224-96c-8-3.4-17.2-3.4-25.2 0zM128 224l-64 0 0 196.3c-.6 .3-1.2 .7-1.8 1.1l-48 32c-11.7 7.8-17 22.4-12.9 35.9S17.9 512 32 512l448 0c14.1 0 26.5-9.2 30.6-22.7s-1.1-28.1-12.9-35.9l-48-32c-.6-.4-1.2-.7-1.8-1.1L448 224l-64 0 0 192-40 0 0-192-64 0 0 192-48 0 0-192-64 0 0 192-40 0 0-192z"/></svg>
              <span>Transferência</span>
            </button>
          </div>
        </div>

        <!-- 2. CATEGORIA DA CONTRIBUIÇÃO (DROPDOWN ESTILIZADA) -->
        <div v-if="!mbwayStatus && !loading" class="mb-6 relative" ref="categoryPickerRef">
          <label class="block text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">
            Destino da Contribuição
          </label>

          <button
            id="donation-category"
            type="button"
            class="relative w-full rounded-2xl bg-gray-50 hover:bg-gray-100/80 px-4 py-3 text-left shadow-sm outline-none transition-all duration-200 cursor-pointer border border-gray-200 focus:border-primary focus:ring-4 focus:ring-primary/10 flex items-center justify-between"
            @click="toggleCategoryDropdown"
            @blur="handleCategoryButtonBlur"
          >
            <span :class="selectedCategory ? 'text-gray-900 font-semibold' : 'text-gray-400 font-medium'">
              {{ selectedCategory || 'Seleciona a categoria' }}
            </span>

            <span class="flex items-center text-gray-400">
              <svg :class="['w-3.5 h-3.5 fill-current transition-transform duration-200', showCategoryDropdown ? 'rotate-180' : '']" viewBox="0 0 512 512" aria-hidden="true"><path d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z"/></svg>
            </span>
          </button>

          <transition name="fade-scale">
            <div
              v-if="showCategoryDropdown"
              class="absolute z-30 mt-2 w-full overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-xl"
            >
              <div class="max-h-60 overflow-y-auto py-2">
                <button
                  v-for="cat in availableCategories"
                  :key="cat.id || cat.name"
                  type="button"
                  class="w-full px-4 py-3 text-left transition-colors duration-200 cursor-pointer flex items-center justify-between hover:bg-sky-50"
                  :class="selectedCategory === cat.name ? 'bg-sky-50/70 font-semibold text-primary' : 'text-gray-800'"
                  @mousedown.prevent="selectCategory(cat.name)"
                >
                  <div class="font-medium text-sm">
                    {{ cat.name }}
                  </div>
                  <svg v-if="selectedCategory === cat.name" class="w-3.5 h-3.5 fill-current text-primary" viewBox="0 0 448 512" aria-hidden="true"><path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- ══════════════════ FLUXO MB WAY: ESTADOS INTERATIVOS ══════════════════ -->
        
        <!-- 1. A AGUARDAR AUTORIZAÇÃO NA APP MB WAY -->
        <div v-if="mbwayStatus === 'waiting'" class="text-center py-6 space-y-5">
          <div class="relative w-16 h-16 mx-auto flex items-center justify-center">
            <span class="absolute inset-0 rounded-full bg-primary/20 animate-ping"></span>
            <div class="relative w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center text-2xl shadow-inner border border-primary/20">
              <svg class="w-6 h-6 fill-current" viewBox="0 0 384 512" aria-hidden="true"><path d="M16 64C16 28.7 44.7 0 80 0L304 0c35.3 0 64 28.7 64 64l0 384c0 35.3-28.7 64-64 64L80 512c-35.3 0-64-28.7-64-64L16 64zM224 448a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zM304 64L80 64l0 320 224 0 0-320z"/></svg>
            </div>
          </div>

          <div>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Aguardando autorização...</h2>
            <p class="text-xs sm:text-sm text-gray-600 mt-2 max-w-sm mx-auto">
              Enviámos um pedido MB WAY no valor de <strong>{{ amount }}€</strong> para <strong>{{ selectedCategory }}</strong>.
            </p>
          </div>

          <div class="p-4 bg-sky-50 rounded-2xl text-sky-950 text-xs sm:text-sm border border-sky-200 text-left flex items-start gap-3">
            <svg class="w-4 h-4 mt-0.5 fill-current text-sky-600 flex-shrink-0 animate-pulse" viewBox="0 0 512 512" aria-hidden="true"><path d="M256 0a256 256 0 1 1 0 512A256 256 0 1 1 256 0zM232 120l0 136c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2 280 120c0-13.3-10.7-24-24-24s-24 10.7-24 24z"/></svg>
            <div class="w-full">
              <div class="flex items-center justify-between">
                <p class="font-bold text-sky-900">Abre a App MB WAY no telemóvel:</p>
                <span class="font-mono font-bold text-xs bg-sky-200/70 text-sky-800 px-2 py-0.5 rounded-full">
                  {{ formattedRemainingTime }}
                </span>
              </div>
              <p class="mt-1 text-sky-800">
                Confirma o pedido na app MB WAY. O temporizador limita apenas a consulta automática nesta página.
              </p>
            </div>
          </div>

          <div class="flex items-center justify-center gap-2 text-xs text-gray-400 py-1">
            <svg class="w-3.5 h-3.5 fill-current animate-spin text-primary" viewBox="0 0 512 512" aria-hidden="true"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0z"/></svg>
            <span>A verificar confirmação em tempo real...</span>
          </div>
        </div>

        <!-- 2. SUCESSO / PAGAMENTO CONFIRMADO (MENSAGEM DE AGRADECIMENTO) -->
        <div v-else-if="mbwayStatus === 'success'" class="text-center py-6 space-y-5">
          <div class="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-3xl shadow-inner animate-bounce">
            <svg class="w-8 h-8 fill-current" viewBox="0 0 512 512" aria-hidden="true"><path d="M47.6 300.4L228.3 469.1c7.5 7 17.4 10.9 27.7 10.9s20.2-3.9 27.7-10.9L464.4 300.4c30.4-28.3 47.6-68 47.6-109.5v-5.8c0-69.9-50.5-129.5-119.4-141C347 36.5 300.6 51.4 268 84L256 96 244 84c-32.6-32.6-79-47.5-124.6-39.9C50.5 55.6 0 115.2 0 185.1v5.8c0 41.5 17.2 81.2 47.6 109.5z"/></svg>
          </div>

          <div>
            <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 mb-2">
              ✓ Pagamento Confirmado
            </span>
            <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Muito Obrigado pela Tua Generosidade!</h2>
            <p class="text-xs sm:text-sm text-gray-600 mt-2 max-w-sm mx-auto">
              Recebemos com gratidão o teu donativo de <strong>{{ amount }}€</strong> para <strong>{{ selectedCategory }}</strong>.
            </p>
          </div>

          <div class="p-4 bg-emerald-50 rounded-2xl text-emerald-950 text-xs sm:text-sm border border-emerald-200 text-left space-y-2">
            <div class="flex items-start gap-2.5">
              “
              <p class="italic text-emerald-900 font-serif text-xs sm:text-sm">
                "Cada um dê conforme determinou no seu coração, não com tristeza ou por necessidade, pois Deus ama a quem dá com alegria."
              </p>
            </div>
            <p class="pt-1 text-[11px] text-emerald-700 border-t border-emerald-200/60 font-medium">
              Para solicitar um recibo, contacta a tesouraria: <strong>{{ donationsConfig.treasuryEmail }}</strong>.
            </p>
          </div>

          <div class="space-y-2.5 pt-2">
            <button
              type="button"
              @click="resetForm"
              class="w-full py-3.5 px-4 rounded-2xl bg-primary text-white font-bold hover:bg-primary/90 transition shadow-lg cursor-pointer text-sm"
            >
              Fazer outra contribuição
            </button>
            <router-link
              to="/"
              class="block w-full py-2.5 px-4 rounded-xl text-xs sm:text-sm font-semibold text-gray-500 hover:text-gray-800 transition"
            >
              Voltar à página inicial
            </router-link>
          </div>
        </div>

        <!-- 3. PAGAMENTO REJEITADO PELO UTILIZADOR (STATUS 020) -->
        <div v-else-if="mbwayStatus === 'rejected'" class="text-center py-6 space-y-5">
          <div class="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto text-2xl shadow-inner">
            ✕
          </div>

          <div>
            <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 mb-2">
              ✕ Operação Cancelada
            </span>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Transferência Rejeitada</h2>
            <p class="text-xs sm:text-sm text-gray-600 mt-2 max-w-sm mx-auto">
              A transferência foi rejeitada ou cancelada na aplicação MB WAY.
            </p>
          </div>

          <div class="p-4 bg-amber-50/80 rounded-2xl text-amber-950 text-xs sm:text-sm border border-amber-200 text-left space-y-2">
            <p class="font-bold text-amber-900 flex items-center gap-1.5">
               Possíveis motivos:
            </p>
            <ul class="list-disc pl-4 text-xs text-amber-800 space-y-1">
              <li>Toque involuntário no botão de rejeitar na aplicação MB WAY;</li>
              <li>Engano no número de telemóvel ou valor introduzido;</li>
              <li>Cancelamento intencional da contribuição.</li>
            </ul>
            <p class="text-[11px] text-amber-700/90 pt-1 border-t border-amber-200/60">
              Nenhum valor foi debitado. Podes alterar os dados ou tentar novamente quando quiseres.
            </p>
          </div>

          <div class="space-y-2.5 pt-2">
            <button
              type="button"
              @click="retryPayment"
              class="w-full py-3.5 px-4 rounded-2xl bg-primary text-white font-bold hover:bg-primary/90 transition shadow-lg cursor-pointer text-sm"
            >
              Tentar novamente
            </button>
            <button
              type="button"
              @click="paymentMethod = 'bank_transfer'; retryPayment()"
              class="w-full py-2.5 px-4 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs sm:text-sm font-semibold transition cursor-pointer"
            >
              Contribuir por transferência bancária
            </button>
          </div>
        </div>

        <!-- 4. TEMPO LIMITE EXPIRADO (STATUS 101 / TIMEOUT) -->
        <div v-else-if="mbwayStatus === 'expired'" class="text-center py-6 space-y-5">
          <div class="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto text-2xl shadow-inner">
            ⏱
          </div>

          <div>
            <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 mb-2">
              ⌛ Prazo Esgotado
            </span>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Tempo Limite Expirado</h2>
            <p class="text-xs sm:text-sm text-gray-600 mt-2 max-w-sm mx-auto">
              O prazo de 4 minutos para autorizar o pagamento no MB WAY terminou sem confirmação.
            </p>
          </div>

          <div class="p-4 bg-sky-50/80 rounded-2xl text-sky-950 text-xs sm:text-sm border border-sky-200 text-left space-y-2">
            <p class="font-bold text-sky-900 flex items-center gap-1.5">
               O que deves saber:
            </p>
            <ul class="list-disc pl-4 text-xs text-sky-800 space-y-1">
              <li>Nenhum valor foi debitado da tua conta bancária;</li>
              <li>A rede MB WAY define um limite de segurança de 4 minutos para cada pedido;</li>
              <li>Certifica-te de que tens as notificações da app MB WAY ativas para receber o alerta de imediato.</li>
            </ul>
          </div>

          <div class="space-y-2.5 pt-2">
            <button
              type="button"
              @click="retryPayment"
              class="w-full py-3.5 px-4 rounded-2xl bg-primary text-white font-bold hover:bg-primary/90 transition shadow-lg cursor-pointer text-sm"
            >
              Enviar novo pedido MB WAY
            </button>
            <button
              type="button"
              @click="paymentMethod = 'bank_transfer'; retryPayment()"
              class="w-full py-2.5 px-4 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs sm:text-sm font-semibold transition cursor-pointer"
            >
              Contribuir por transferência bancária
            </button>
          </div>
        </div>

        <!-- 5. TRANSAÇÃO RECUSADA PELA ENTIDADE / BANCO (STATUS 122) -->
        <div v-else-if="mbwayStatus === 'declined'" class="text-center py-6 space-y-5">
          <div class="w-16 h-16 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto text-2xl shadow-inner">
            ⚠
          </div>

          <div>
            <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 mb-2">
              ✕ Não Autorizado
            </span>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Transação Não Autorizada</h2>
            <p class="text-xs sm:text-sm text-gray-600 mt-2 max-w-sm mx-auto">
              A entidade bancária ou emissora do teu MB WAY não autorizou esta operação.
            </p>
          </div>

          <div class="p-4 bg-rose-50/80 rounded-2xl text-rose-950 text-xs sm:text-sm border border-rose-200 text-left space-y-2">
            <p class="font-bold text-rose-900 flex items-center gap-1.5">
               Possíveis causas:
            </p>
            <ul class="list-disc pl-4 text-xs text-rose-800 space-y-1">
              <li>Saldo insuficiente na conta bancária associada ao MB WAY;</li>
              <li>Limite diário ou mensal de pagamentos MB WAY atingido;</li>
              <li>Cartão de pagamento inativo, bloqueado ou expirado.</li>
            </ul>
          </div>

          <div class="space-y-2.5 pt-2">
            <button
              type="button"
              @click="retryPayment"
              class="w-full py-3.5 px-4 rounded-2xl bg-primary text-white font-bold hover:bg-primary/90 transition shadow-lg cursor-pointer text-sm"
            >
              Tentar novamente
            </button>
            <button
              type="button"
              @click="paymentMethod = 'bank_transfer'; retryPayment()"
              class="w-full py-2.5 px-4 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs sm:text-sm font-semibold transition cursor-pointer"
            >
              Contribuir por transferência bancária
            </button>
          </div>
        </div>

        <div v-else-if="mbwayStatus === 'unknown'" class="text-center py-6 space-y-4">
          <h2 class="text-xl font-bold text-gray-900">Estado do pagamento por confirmar</h2>
          <p class="text-sm text-gray-600">Não foi possível confirmar o resultado. Verifica a app MB WAY e os movimentos bancários. Não inicies outro pagamento até confirmares este pedido com a tesouraria.</p>
          <p class="text-sm text-gray-700">Contacto: <strong>{{ donationsConfig.treasuryEmail }}</strong></p>
          <p v-if="savedAttempt" class="text-xs text-gray-500 break-all">Referência do pedido: {{ savedAttempt.key }}</p>
          <p v-if="errorMessage" class="text-xs text-red-700">{{ errorMessage }}</p>
          <div class="space-y-2.5 pt-2">
            <button type="button" :disabled="loading || !savedAttempt" @click="recoverPayment" class="w-full py-3 rounded-xl bg-primary text-white font-semibold disabled:opacity-50 cursor-pointer">Verificar o mesmo pedido</button>
            <button type="button" @click="discardUnknownPayment" class="w-full py-2.5 px-4 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs sm:text-sm font-semibold transition cursor-pointer">Já verifiquei na App MB WAY — Iniciar novo pedido</button>
          </div>
        </div>

        <!-- ══════════════════ FLUXO 1: MB WAY ══════════════════ -->
        <form v-else-if="paymentMethod === 'mbway'" @submit.prevent="submitMbway" class="space-y-6">
          
          <!-- SELETOR DE VALORES (ESTILO APP FINANCEIRA) -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-xs font-bold uppercase tracking-wider text-gray-500">
                Valor a Contribuir
              </label>
              <span class="text-xs text-primary font-semibold">Moeda: EUR (€)</span>
            </div>

            <!-- Campo de Valor em Destaque -->
            <div class="relative bg-gray-50 rounded-2xl border border-gray-200 p-4 mb-3 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 transition-all flex items-center justify-center">
              <span class="text-3xl sm:text-4xl font-extrabold text-gray-400 mr-2">€</span>
              <input
                type="number"
                v-model="amount"
                step="0.50"
                min="0.5"
                required
                class="w-40 text-center text-3xl sm:text-4xl font-extrabold text-gray-900 bg-transparent outline-none tracking-tight"
                placeholder="0.00"
              />
            </div>

            <!-- Botões de Valor Rápido -->
            <div class="grid grid-cols-4 gap-2">
              <button
                v-for="val in quickAmounts"
                :key="val"
                type="button"
                @click="amount = String(val)"
                class="py-2 px-2 rounded-xl text-xs sm:text-sm font-bold transition-all cursor-pointer border"
                :class="[
                  Number(amount) === val
                    ? 'bg-gray-900 text-white border-gray-900 shadow-md scale-[1.02]'
                    : 'bg-gray-50 hover:bg-gray-100 text-gray-700 border-gray-200'
                ]"
              >
                {{ val }}€
              </button>
            </div>
          </div>

          <!-- NÚMERO DE TELEMÓVEL MB WAY -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-500">
                Número de Telemóvel (MB WAY)
              </label>
              <span class="text-[11px] text-gray-400">9 dígitos</span>
            </div>
            <div class="relative rounded-2xl shadow-sm">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 512 512" aria-hidden="true"><path d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>
              </div>
              <input
                type="tel"
                v-model="phone"
                required
                maxlength="13"
                placeholder="Ex: 912 345 678"
                class="block w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl text-sm font-semibold text-gray-900 placeholder:text-gray-400 focus:ring-2 focus:ring-primary/20 focus:border-primary transition outline-none"
              />
            </div>
          </div>

          <div class="p-4 bg-gray-50 rounded-2xl border border-gray-200 text-xs text-gray-600">
            Para solicitar um recibo, contacta a tesouraria após o pagamento:
            <strong>{{ donationsConfig.treasuryEmail }}</strong>. O formulário não emite recibos automaticamente.
          </div>

          <!-- CHECKBOX DE CONSENTIMENTO LEGAL (OBRIGATÓRIO PARA COMPLIANCE) -->
          <div class="pt-2">
            <label class="flex items-start gap-2.5 text-xs text-gray-600 cursor-pointer select-none">
              <input
                type="checkbox"
                v-model="termsAccepted"
                required
                class="mt-0.5 rounded border-gray-300 text-primary focus:ring-primary h-4 w-4 cursor-pointer"
              />
              <span>
                Li e aceito os
                <router-link to="/termos-e-condicoes" target="_blank" class="text-primary font-semibold hover:underline">Termos e Condições</router-link>
                e a
                <router-link to="/politica-privacidade" target="_blank" class="text-primary font-semibold hover:underline">Política de Privacidade</router-link>.
              </span>
            </label>
          </div>

          <!-- Mensagem de Erro -->
          <div v-if="errorMessage" class="rounded-2xl bg-rose-50 p-3.5 border border-rose-200 text-rose-700 text-xs sm:text-sm flex items-start gap-2.5">
            <svg class="w-4 h-4 mt-0.5 fill-current flex-shrink-0" viewBox="0 0 512 512" aria-hidden="true"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24l0 112c0 13.3-10.7 24-24 24s-24-10.7-24-24l0-112c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Botão Principal CTA -->
          <button
            type="submit"
            :disabled="loading || !amount || !phone || !termsAccepted"
            class="w-full flex items-center justify-center gap-2 py-4 px-6 rounded-2xl shadow-xl text-base font-bold text-white bg-primary hover:bg-primary/90 active:scale-[0.99] transition-all disabled:opacity-50 cursor-pointer"
          >
            <span v-if="loading" class="flex items-center gap-2">
              <svg class="w-4 h-4 fill-current animate-spin" viewBox="0 0 512 512" aria-hidden="true"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0z"/></svg>
              A processar...
            </span>
            <span v-else class="flex items-center gap-2">
              <span>Contribuir {{ amount ? `${amount}€` : '' }} via MB WAY</span>
              <svg class="w-3 h-3 fill-current" viewBox="0 0 448 512" aria-hidden="true"><path d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z"/></svg>
            </span>
          </button>

          <!-- Nota de Enquadramento Fiscal -->
          <p class="text-[11px] text-gray-400 text-center leading-relaxed">
            Donativo voluntário sem fins comerciais. Isenção de IVA (art. 9.º do CIVA).
          </p>
        </form>

        <!-- ══════════════════ FLUXO 2: TRANSFERÊNCIA BANCÁRIA ══════════════════ -->
        <div v-else-if="paymentMethod === 'bank_transfer'" class="space-y-5">
          
          <!-- Card de Dados Bancários com design tipo Cartão de Conta -->
          <div class="bg-gradient-to-br from-slate-900 to-slate-800 text-white rounded-2xl p-5 shadow-lg space-y-4">
            <div class="flex items-center justify-between border-b border-white/10 pb-3">
              <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Conta Oficial ICMAV</span>
              <span class="text-xs font-bold text-white px-2 py-0.5 rounded-full bg-white/10">SEPA</span>
            </div>

            <div>
              <span class="text-[11px] text-gray-400 block font-medium">Titular da Conta</span>
              <span class="font-bold text-sm sm:text-base text-white">
                {{ donationsConfig.beneficiary || 'Igreja Cristã Manancial de Águas Vivas' }}
              </span>
            </div>

            <div>
              <span class="text-[11px] text-gray-400 block font-medium mb-1">IBAN</span>
              <div class="flex items-center justify-between gap-2 bg-black/40 p-3 rounded-xl border border-white/10">
                <span class="font-mono font-bold text-xs sm:text-sm text-emerald-300 break-all">
                  {{ donationsConfig.iban || 'PT50 0007 0246 0014 0750 0033 4' }}
                </span>
                <button
                  type="button"
                  @click="copyIban"
                  class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold transition cursor-pointer flex-shrink-0"
                >
                  {{ copiedIban ? 'Copiado! ✓' : 'Copiar' }}
                </button>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3 pt-1 text-xs">
              <div>
                <span class="text-gray-400 block">Banco</span>
                <span class="font-semibold text-white">{{ donationsConfig.bank || 'NOVO BANCO, SA' }}</span>
              </div>
              <div>
                <span class="text-gray-400 block">BIC / SWIFT</span>
                <span class="font-semibold text-white">{{ donationsConfig.bic || 'BESCPTPLXXX' }}</span>
              </div>
            </div>
          </div>

          <!-- Nota de Descritivo -->
          <div class="p-3.5 bg-indigo-50 rounded-2xl text-indigo-900 text-xs sm:text-sm border border-indigo-100 flex items-start gap-2.5">
            <svg class="w-4 h-4 mt-0.5 fill-current text-primary flex-shrink-0" viewBox="0 0 512 512" aria-hidden="true"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM216 336l24 0 0-64-24 0c-13.3 0-24-10.7-24-24s10.7-24 24-24l48 0c13.3 0 24 10.7 24 24l0 88 8 0c13.3 0 24 10.7 24 24s-10.7 24-24 24l-80 0c-13.3 0-24-10.7-24-24s10.7-24 24-24zm40-208a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>
            <div>
              <p class="font-bold">Descritivo sugerido:</p>
              <p class="mt-0.5 text-xs text-indigo-800">
                Indica <strong>{{ selectedCategory }}</strong> no descritivo da transferência.
              </p>
            </div>
          </div>

          <!-- Emissão de Recibo por Email -->
          <div class="p-4 bg-gray-50 rounded-2xl border border-gray-200 text-xs text-gray-600 space-y-1.5">
            <p class="font-semibold text-gray-800">Para obter recibo fiscal:</p>
            <p>
              Envia o comprovativo da transferência para:
              <a :href="`mailto:${donationsConfig.treasuryEmail || 'tesouraria.icmav@gmail.com'}`" class="text-primary font-bold hover:underline">
                {{ donationsConfig.treasuryEmail || 'tesouraria.icmav@gmail.com' }}
              </a>
            </p>
            <p class="text-xs text-gray-800 font-medium">
              Inclui Nome Completo, NIF e Morada de Faturação.
            </p>
          </div>

        </div>

      </div>

      <!-- ══════════════════ RODAPÉ DE CONFIANÇA & LINKS LEGAIS ══════════════════ -->
      <footer class="mt-6 text-center text-[11px] text-gray-400 space-y-2">
        <p class="flex items-center justify-center gap-1.5 font-medium text-emerald-400">
          <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 512 512" aria-hidden="true"><path d="M256 0c4.6 0 9.2 1 13.4 2.9L457.7 82.8c22 9.3 38.4 31 38.3 57.2c-.5 99.2-41.3 280.7-213.6 363.2c-16.7 8-36.1 8-52.8 0C57.3 420.7 16.5 239.2 16 140c-.1-26.2 16.3-47.9 38.3-57.2L242.7 2.9C246.8 1 251.4 0 256 0zm0 66.8l0 378.1C394 378 431.1 230.1 432 141.4L256 66.8l0 0z"/></svg>
          <span>Processamento Seguro e Certificado via IFTHENPAY / MB WAY</span>
        </p>
        <!-- Links de Políticas no Rodapé do Formulário -->
        <div class="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-gray-400">
          <router-link to="/termos-e-condicoes" target="_blank" class="hover:text-white transition-colors">Termos e Condições</router-link>
          <span>•</span>
          <router-link to="/politica-privacidade" target="_blank" class="hover:text-white transition-colors">Privacidade (RGPD)</router-link>
          <span>•</span>
          <router-link to="/politica-cookies" target="_blank" class="hover:text-white transition-colors">Política de Cookies</router-link>
          <span>•</span>
          <router-link to="/politica-cancelamento-reembolso" target="_blank" class="hover:text-white transition-colors">Cancelamento e Reembolsos</router-link>
        </div>
        <p class="text-gray-400 font-semibold">&copy; {{ copyrightText }}</p>
      </footer>

    </main>

    <!-- Espaçamento inferior harmonioso -->
    <div class="h-6"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { submitDonationMbway, recoverDonationAttempt, getPaymentStatus, getDonationsContent } from '../services/api'
import { beginPayment, readPayment, updatePayment, clearConfirmedPayment, dismissUnknownAttempt, classifyPaymentStatus } from '../utils/payment-state'
import logoWhite from '../assets/logo_provisory_white.png'
import MbwayLogo from '../components/icons/MbwayLogo.vue'

const quickAmounts = [10, 20, 50, 100]

const paymentMethod = ref('mbway') // 'mbway' | 'bank_transfer'
const selectedCategory = ref('Ofertas')
const showCategoryDropdown = ref(false)
const categoryPickerRef = ref(null)
const termsAccepted = ref(false)

function toggleCategoryDropdown() {
  showCategoryDropdown.value = !showCategoryDropdown.value
}

function selectCategory(categoryName) {
  selectedCategory.value = categoryName
  showCategoryDropdown.value = false
}

function handleCategoryButtonBlur() {
  setTimeout(() => {
    showCategoryDropdown.value = false
  }, 150)
}

function handleClickOutside(event) {
  if (categoryPickerRef.value && !categoryPickerRef.value.contains(event.target)) {
    showCategoryDropdown.value = false
  }
}

const initialDonations =
  typeof window !== 'undefined' && window.__INITIAL_DONATIONS__
    ? window.__INITIAL_DONATIONS__.value || window.__INITIAL_DONATIONS__
    : null

const donationsConfig = ref({
  beneficiary: 'Igreja Cristã Manancial de Águas Vivas',
  iban: 'PT50 0007 0246 0014 0750 0033 4',
  bank: 'NOVO BANCO, SA',
  bic: 'BESCPTPLXXX',
  treasuryEmail: 'tesouraria.icmav@gmail.com',
  categories: [
    { id: 'Ofertas', name: 'Ofertas' },
    { id: 'Dízimos', name: 'Dízimos' },
    { id: 'Missões', name: 'Missões' },
  ],
  ...(initialDonations && typeof initialDonations === 'object' ? initialDonations : {}),
})

if (Array.isArray(donationsConfig.value.categories) && donationsConfig.value.categories.length > 0) {
  selectedCategory.value = donationsConfig.value.categories[0].name
}

const availableCategories = computed(() => {
  if (Array.isArray(donationsConfig.value.categories) && donationsConfig.value.categories.length > 0) {
    return donationsConfig.value.categories
  }
  return [
    { id: 'Ofertas', name: 'Ofertas' },
    { id: 'Dízimos', name: 'Dízimos' },
    { id: 'Missões', name: 'Missões' },
  ]
})

const amount = ref('')
const phone = ref('')

const loading = ref(false)
const errorMessage = ref('')
const copiedIban = ref(false)

// Estados do fluxo MB WAY: null | 'waiting' | 'success' | 'rejected' | 'expired' | 'declined' | 'unknown'
const mbwayStatus = ref(null)
const savedAttempt = ref(null)
let checkingStatus = false
const currentRequestId = ref(null)
const remainingSeconds = ref(240)
let pollInterval = null
let countdownTimer = null

const formattedRemainingTime = computed(() => {
  const mins = Math.floor(remainingSeconds.value / 60)
  const secs = remainingSeconds.value % 60
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`
})

function stopPolling() {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

function savePaymentState(state, requestId) {
  mbwayStatus.value = state
  try {
    savedAttempt.value = updatePayment(sessionStorage, { state, requestId })
  } catch {
    // An existing in-memory attempt still prevents another submission in this view.
    errorMessage.value = 'Não foi possível guardar o estado. Contacta a tesouraria antes de repetir o pagamento.'
  }
}

async function checkPaymentStatusNow() {
  if (!currentRequestId.value || checkingStatus) return
  checkingStatus = true
  try {
    const res = await getPaymentStatus(currentRequestId.value, savedAttempt.value.key)
    let state = classifyPaymentStatus(res)
    if (state === 'waiting' && remainingSeconds.value === 0) state = 'expired'
    if (['success', 'rejected', 'expired', 'declined'].includes(state)) {
      stopPolling()
      savePaymentState(state)
    } else if (remainingSeconds.value > 0 && mbwayStatus.value === 'waiting') {
      // Keep waiting while timer is active unless a terminal status arrives
      savePaymentState('waiting')
    } else {
      stopPolling()
      savePaymentState(state)
    }
  } catch {
    // Transient network/rate-limit errors while timer is running should not interrupt the timer
    if (mbwayStatus.value !== 'waiting' || remainingSeconds.value === 0) {
      stopPolling()
      savePaymentState('unknown')
    }
  } finally {
    checkingStatus = false
  }
}

function startPolling(requestId) {
  stopPolling()
  currentRequestId.value = requestId
  remainingSeconds.value = Math.max(0, 240 - Math.floor((Date.now() - savedAttempt.value.startedAt) / 1000))
  savePaymentState(remainingSeconds.value ? 'waiting' : 'expired', requestId)
  if (!remainingSeconds.value) {
    checkPaymentStatusNow()
    return
  }
  countdownTimer = setInterval(() => {
    remainingSeconds.value = Math.max(0, remainingSeconds.value - 1)
    if (remainingSeconds.value === 0) {
      stopPolling()
      savePaymentState('expired')
    }
  }, 1000)
  pollInterval = setInterval(checkPaymentStatusNow, 1000)
}

function retryPayment() {
  if (!['rejected', 'expired', 'declined'].includes(mbwayStatus.value)) return
  try {
    clearConfirmedPayment(sessionStorage)
  } catch {
    errorMessage.value = 'Não foi possível reiniciar o pedido. Contacta a tesouraria.'
    return
  }
  stopPolling()
  savedAttempt.value = null
  currentRequestId.value = null
  mbwayStatus.value = null
  errorMessage.value = ''
}

function discardUnknownPayment() {
  try {
    dismissUnknownAttempt(sessionStorage)
  } catch {
    // ignore
  }
  stopPolling()
  savedAttempt.value = null
  currentRequestId.value = null
  mbwayStatus.value = null
  errorMessage.value = ''
}

async function recoverPayment() {
  if (!savedAttempt.value || loading.value) return
  loading.value = true
  try {
    if (currentRequestId.value) {
      startPolling(currentRequestId.value)
      await checkPaymentStatusNow()
    } else {
      const result = await recoverDonationAttempt(savedAttempt.value.key)
      if (!result?.requestId) throw new Error('Unknown payment')
      startPolling(result.requestId)
    }
  } catch {
    savePaymentState('unknown')
  } finally {
    loading.value = false
  }
}

const siteOwner = 'ICMAV'
const currentYear = new Date().getFullYear()

const copyrightText = `${siteOwner} ${currentYear}`

function copyIban() {
  const clean = (donationsConfig.value.iban || 'PT50003300004547387123405').replace(/\s+/g, '')
  navigator.clipboard.writeText(clean)
  copiedIban.value = true
  setTimeout(() => {
    copiedIban.value = false
  }, 2500)
}

function resetForm() {
  if (mbwayStatus.value !== 'success') return
  try {
    clearConfirmedPayment(sessionStorage)
  } catch {
    errorMessage.value = 'Não foi possível concluir este pedido. Contacta a tesouraria.'
    return
  }
  stopPolling()
  savedAttempt.value = null
  currentRequestId.value = null
  mbwayStatus.value = null
  errorMessage.value = ''
  phone.value = ''
  amount.value = ''
  termsAccepted.value = false
}

async function submitMbway() {
  if (loading.value || mbwayStatus.value || (savedAttempt.value && savedAttempt.value.state !== 'not_sent')) return
  errorMessage.value = ''
  if (savedAttempt.value?.retryAt > Date.now()) {
    errorMessage.value = 'Aguarda alguns minutos antes de tentar novamente. O pedido não foi enviado.'
    return
  }
  if (!termsAccepted.value) {
    errorMessage.value = 'Por favor, aceita os Termos e Condições e a Política de Privacidade para prosseguir.'
    return
  }
  loading.value = true
  try {
    // This write must succeed before any request can reach the payment gateway.
    savedAttempt.value = savedAttempt.value
      ? updatePayment(sessionStorage, { state: 'unknown', amount: amount.value, category: selectedCategory.value })
      : beginPayment(sessionStorage, { amount: amount.value, category: selectedCategory.value })
    const res = await submitDonationMbway(Number(amount.value), phone.value, selectedCategory.value, null, savedAttempt.value.key)
    if (!res?.requestId) throw new Error('Unknown payment')
    startPolling(res.requestId)
  } catch (err) {
    if (savedAttempt.value && err?.response?.attemptState === 'not-sent') {
      // Only the server's explicit absence-of-reservation marker permits retry. Keep the same key.
      const seconds = Number(err.response.retryAfter || 0)
      const delay = Number.isFinite(seconds) && seconds > 0 ? Math.min(seconds, 3600) * 1000 : 0
      savedAttempt.value = updatePayment(sessionStorage, { state: 'not_sent', retryAt: Date.now() + delay })
      mbwayStatus.value = null
      errorMessage.value = 'O pedido não foi enviado. Verifica os dados ou aguarda antes de tentar novamente.'
    } else if (savedAttempt.value) savePaymentState('unknown')
    else errorMessage.value = err.message || 'Não é possível guardar este pedido neste navegador. Nenhum pedido foi enviado.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  try {
    savedAttempt.value = readPayment(sessionStorage)
    if (savedAttempt.value) {
      amount.value = savedAttempt.value.amount
      selectedCategory.value = savedAttempt.value.category
      currentRequestId.value = savedAttempt.value.requestId
      const restoredState = savedAttempt.value.state
      if (restoredState === 'not_sent') {
        mbwayStatus.value = null
      } else if (['success', 'rejected', 'expired', 'declined'].includes(restoredState)) {
        mbwayStatus.value = restoredState
      } else if (restoredState === 'waiting' && currentRequestId.value) {
        startPolling(currentRequestId.value)
      } else {
        mbwayStatus.value = 'unknown'
        await recoverPayment()
      }
    }
  } catch {
    mbwayStatus.value = 'unknown'
    errorMessage.value = 'Não foi possível recuperar o pedido guardado. Contacta a tesouraria antes de repetir.'
  }

  if (!initialDonations) {
    try {
      const res = await getDonationsContent()
      const data = res?.value || res
      if (data && typeof data === 'object') {
        donationsConfig.value = {
          ...donationsConfig.value,
          ...data,
        }
        if (!savedAttempt.value && Array.isArray(data.categories) && data.categories.length > 0) {
          selectedCategory.value = data.categories[0].name
        }
      }
    } catch {
      // Silenciosamente mantém os defaults
    }
  }
})

onBeforeUnmount(() => {
  stopPolling()
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-69px);
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.96) translateY(-6px);
}
</style>
