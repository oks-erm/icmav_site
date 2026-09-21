<!-- src/views/CookiePolicyView.vue -->
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
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30 mb-3">
          <i class="fa-solid fa-cookie-bite text-xs"></i>
          Regulamentação e-Privacy & RGPD
        </span>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Política de Cookies
        </h1>
        <p class="mt-2 text-sm text-gray-400">
          Última atualização: Setembro de 2025 • Em conformidade com a Lei n.º 41/2004, alterada pela Lei n.º 46/2012 e o Regulamento Geral sobre a Proteção de Dados (RGPD).
        </p>
      </div>

      <!-- Conteúdo Estruturado -->
      <div class="space-y-8 text-sm sm:text-base text-gray-300 leading-relaxed">
        
        <!-- Secção 1: O que são cookies -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">1.</span>
            O que são Cookies?
          </h2>
          <p class="mb-3">
            Os <em>cookies</em> são pequenos ficheiros de texto com informação relevante que são descarregados e armazenados no seu dispositivo (computador, smartphone ou tablet) através do seu navegador de internet (browser) quando visita um sítio web.
          </p>
          <p>
            A utilização de cookies permite que o sítio web reconheça o seu dispositivo em visitas futuras, guarde as suas preferências de navegação e proporcione uma navegação mais eficiente, segura e personalizada.
          </p>
        </section>

        <!-- Secção 2: Entidade Responsável -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">2.</span>
            Entidade Responsável pelo Tratamento
          </h2>
          <p class="mb-3">
            O presente sítio web é gerido pela <strong>Igreja Cristã Manancial de Águas Vivas (ICMAV)</strong>, com os seguintes dados institucionais:
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300">
            <li><strong>Denominação:</strong> Igreja Cristã Manancial de Águas Vivas (ICMAV)</li>
            <li><strong>NIPC:</strong> 592 002 403</li>
            <li><strong>Sede:</strong> Estrada de Polima N.º 609, 2785-303 São Domingos de Rana, Portugal</li>
            <li><strong>E-mail de Contacto:</strong> <a href="mailto:ccicmav@gmail.com" class="text-amber-400 hover:underline">ccicmav@gmail.com</a></li>
          </ul>
        </section>

        <!-- Secção 3: Tipos de Cookies Utilizados -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">3.</span>
            Categorias de Cookies Utilizados
          </h2>
          <p class="mb-4">
            No website da ICMAV utilizamos as seguintes categorias de cookies e tecnologias de armazenamento local:
          </p>

          <div class="space-y-4">
            <!-- Categoria A -->
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5 space-y-2">
              <h3 class="font-bold text-white text-base flex items-center gap-2">
                <i class="fa-solid fa-shield-halved text-emerald-400 text-sm"></i>
                A. Cookies Estritamente Necessários / Técnicos
              </h3>
              <p class="text-xs sm:text-sm text-gray-300">
                São indispensáveis para o funcionamento básico e segurança do sítio web. Permitem a navegação pelas páginas, a autenticação segura na área administrativa e a retenção do seu consentimento de privacidade. Não recolhem informação para efeitos de marketing e não podem ser desativados nos nossos sistemas.
              </p>
            </div>

            <!-- Categoria B -->
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5 space-y-2">
              <h3 class="font-bold text-white text-base flex items-center gap-2">
                <i class="fa-solid fa-sliders text-primary text-sm"></i>
                B. Cookies de Funcionalidade e Preferências
              </h3>
              <p class="text-xs sm:text-sm text-gray-300">
                Permitem recordar as opções e preferências selecionadas pelo utilizador (como idioma, localização pré-selecionada ou estado do formulário de donativos) para proporcionar uma experiência de utilização mais conveniente.
              </p>
            </div>

            <!-- Categoria C -->
            <div class="p-4 bg-gray-800/60 rounded-xl border border-white/5 space-y-2">
              <h3 class="font-bold text-white text-base flex items-center gap-2">
                <i class="fa-solid fa-map-location-dot text-indigo-400 text-sm"></i>
                C. Cookies de Terceiros e Serviços Externos
              </h3>
              <p class="text-xs sm:text-sm text-gray-300">
                Podem ser instalados por serviços de entidades terceiras integradas no nosso website para disponibilizar funcionalidades adicionais, tais como:
              </p>
              <ul class="text-xs sm:text-sm text-gray-300 list-disc pl-5 space-y-1">
                <li><strong>Google Maps:</strong> Para exibição interativa da localização das nossas igrejas e extensões.</li>
                <li><strong>Gateway de Pagamentos / SIBS:</strong> Para o encaminhamento e liquidação segura dos pedidos de pagamento via MB WAY.</li>
                <li><strong>FontAwesome / Fontes Google:</strong> Para a renderização tipográfica e iconográfica otimizada.</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Secção 4: Tabela detalhada de Cookies -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">4.</span>
            Tabela de Cookies e Armazenamento Local
          </h2>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs sm:text-sm border-collapse">
              <thead>
                <tr class="border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-[11px]">
                  <th class="py-3 px-3">Nome / Chave</th>
                  <th class="py-3 px-3">Origem</th>
                  <th class="py-3 px-3">Finalidade</th>
                  <th class="py-3 px-3">Duração</th>
                  <th class="py-3 px-3">Tipo</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5 text-gray-300">
                <tr>
                  <td class="py-3 px-3 font-mono font-medium text-white">icmav_cookie_consent</td>
                  <td class="py-3 px-3">ICMAV (Próprio)</td>
                  <td class="py-3 px-3">Regista o consentimento do utilizador face à Política de Cookies.</td>
                  <td class="py-3 px-3">1 ano</td>
                  <td class="py-3 px-3">Necessário</td>
                </tr>
                <tr>
                  <td class="py-3 px-3 font-mono font-medium text-white">icmav_admin_token</td>
                  <td class="py-3 px-3">ICMAV (Próprio)</td>
                  <td class="py-3 px-3">Armazena o token JWT de sessão autenticada para acesso ao painel de administração.</td>
                  <td class="py-3 px-3">Sessão / 2h</td>
                  <td class="py-3 px-3">Necessário</td>
                </tr>
                <tr>
                  <td class="py-3 px-3 font-mono font-medium text-white">NID / __Secure-*</td>
                  <td class="py-3 px-3">Google (Maps)</td>
                  <td class="py-3 px-3">Utilizados pela API do Google Maps para renderizar o mapa interativo de localização da sede e extensões.</td>
                  <td class="py-3 px-3">6 meses</td>
                  <td class="py-3 px-3">Funcional</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Secção 5: Como Gerir ou Desativar Cookies -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">5.</span>
            Como Controlar e Desativar Cookies no seu Navegador
          </h2>
          <p class="mb-3">
            O utilizador pode, a qualquer momento, configurar o seu navegador para aceitar, recusar ou eliminar cookies. No entanto, alertamos que a desativação de cookies estritamente necessários pode impedir o correto funcionamento de certas funcionalidades do website (como o acesso à área de administração ou o envio de donativos).
          </p>
          <p class="mb-3">
            Para gerir os cookies diretamente no seu navegador, consulte as instruções oficiais:
          </p>
          <ul class="space-y-1.5 pl-4 list-disc text-gray-300">
            <li>
              <strong>Google Chrome:</strong> <a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline">Gestão de cookies no Chrome</a>
            </li>
            <li>
              <strong>Mozilla Firefox:</strong> <a href="https://support.mozilla.org/pt-PT/kb/protecao-contra-rastreio-melhorada-firefox-computador" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline">Gestão de cookies no Firefox</a>
            </li>
            <li>
              <strong>Apple Safari:</strong> <a href="https://support.apple.com/pt-pt/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline">Gestão de cookies no Safari</a>
            </li>
            <li>
              <strong>Microsoft Edge:</strong> <a href="https://support.microsoft.com/pt-pt/microsoft-edge/eliminar-cookies-no-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline">Gestão de cookies no Edge</a>
            </li>
          </ul>
        </section>

        <!-- Secção 6: Atualizações à Política de Cookies -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">6.</span>
            Atualizações a esta Política
          </h2>
          <p class="mb-3">
            A ICMAV reserva-se o direito de atualizar ou modificar a presente Política de Cookies a qualquer momento, nomeadamente para dar cumprimento a alterações legislativas ou à introdução de novas ferramentas tecnológicas.
          </p>
          <p>
            Recomendamos a consulta periódica desta página para se manter informado sobre a forma como utilizamos os cookies.
          </p>
        </section>

        <!-- Secção 7: Contactos -->
        <section class="bg-gray-900/60 border border-white/10 rounded-2xl p-6 sm:p-8">
          <h2 class="text-xl font-bold text-white mb-3 flex items-center gap-2.5">
            <span class="text-amber-400 font-mono text-lg">7.</span>
            Dúvidas e Contactos
          </h2>
          <p class="mb-3">
            Caso tenha qualquer dúvida sobre a nossa Política de Cookies ou sobre o tratamento dos seus dados pessoais, entre em contacto connosco através do endereço eletrónico: <a href="mailto:ccicmav@gmail.com" class="text-amber-400 font-bold hover:underline">ccicmav@gmail.com</a> ou consulte a nossa <router-link to="/politica-privacidade" class="text-amber-400 font-semibold hover:underline">Política de Privacidade</router-link>.
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
