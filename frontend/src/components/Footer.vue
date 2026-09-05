<!-- src/components/Footer.vue -->
<template>
  <footer class="bg-gray-900 text-gray-400 border-t border-white/10 pt-12 pb-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 pb-10 border-b border-white/10 text-sm">
      
      <!-- Coluna 1: Sobre & Missão -->
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <img :src="logoWhite" alt="ICMAV" class="h-9 w-auto object-contain" />
        </div>
        <p class="text-gray-400 text-xs sm:text-sm leading-relaxed">
          Igreja Cristã Manancial de Águas Vivas<br>Uma comunidade de fé, família e esperança ao serviço de Deus e do próximo.
        </p>
        <!-- Redes Sociais -->
        <div class="flex items-center gap-3 pt-2">
          <a
            href="https://facebook.com/icmav"
            target="_blank"
            rel="noopener noreferrer"
            class="w-8 h-8 rounded-lg bg-white/5 hover:bg-primary/20 hover:text-primary flex items-center justify-center transition-all text-xs border border-white/10"
            aria-label="Facebook"
          >
            <i class="fa-brands fa-facebook-f"></i>
          </a>
          <a
            href="https://instagram.com/icmav"
            target="_blank"
            rel="noopener noreferrer"
            class="w-8 h-8 rounded-lg bg-white/5 hover:bg-pink-500/20 hover:text-pink-400 flex items-center justify-center transition-all text-xs border border-white/10"
            aria-label="Instagram"
          >
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a
            href="https://www.youtube.com/@igrejaICMAV"
            target="_blank"
            rel="noopener noreferrer"
            class="w-8 h-8 rounded-lg bg-white/5 hover:bg-red-500/20 hover:text-red-400 flex items-center justify-center transition-all text-xs border border-white/10"
            aria-label="YouTube"
          >
            <i class="fa-brands fa-youtube"></i>
          </a>
          <a
            href="https://chat.whatsapp.com/EdGaqNUARdYB7HokXeleHR"
            target="_blank"
            rel="noopener noreferrer"
            class="w-8 h-8 rounded-lg bg-white/5 hover:bg-emerald-500/20 hover:text-emerald-400 flex items-center justify-center transition-all text-xs border border-white/10"
            aria-label="WhatsApp"
          >
            <i class="fa-brands fa-whatsapp"></i>
          </a>
        </div>
      </div>

      <!-- Coluna 2: Dados Institucionais & Contactos -->
      <div class="space-y-3">
        <h3 class="text-white font-bold text-sm uppercase tracking-wider">Identificação & Contactos</h3>
        <ul class="space-y-2 text-xs text-gray-300">
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-church text-primary mt-0.5"></i>
            <span><strong>ICMAV</strong> — Igreja Cristã Manancial de Águas Vivas</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-location-dot text-primary mt-0.5"></i>
            <span>Estrada de Polima N.º 609, 2785-303 São Domingos de Rana</span>
          </li>
          <li class="flex items-center gap-2">
            <i class="fa-solid fa-envelope text-primary"></i>
            <a href="mailto:ccicmav@gmail.com" class="hover:text-white transition-colors">ccicmav@gmail.com</a>
          </li>
          <li class="flex items-center gap-2">
            <i class="fa-solid fa-phone text-primary"></i>
            <a href="tel:+351934693310" class="hover:text-white transition-colors">+351 934 693 310</a>
          </li>
          <li class="pt-1 text-[11px] text-gray-400">
            <i class="fa-solid fa-clock text-gray-400 mr-1"></i>
            Culto Principal: Domingos às 10h30
          </li>
        </ul>
      </div>

      <!-- Coluna 3: Links Legais & Conformidade -->
      <div class="space-y-3">
        <h3 class="text-white font-bold text-sm uppercase tracking-wider">Informação Legal</h3>
        <ul class="space-y-2 text-xs text-gray-300">
          <li>
            <router-link to="/termos-e-condicoes" class="hover:text-primary transition-colors flex items-center gap-1.5">
              <i class="fa-solid fa-file-contract text-gray-400 text-[10px]"></i>
              <span>Termos e Condições</span>
            </router-link>
          </li>
          <li>
            <router-link to="/politica-privacidade" class="hover:text-primary transition-colors flex items-center gap-1.5">
              <i class="fa-solid fa-user-shield text-gray-400 text-[10px]"></i>
              <span>Política de Privacidade (RGPD)</span>
            </router-link>
          </li>
          <li>
            <router-link to="/politica-cancelamento-reembolso" class="hover:text-primary transition-colors flex items-center gap-1.5">
              <i class="fa-solid fa-rotate-left text-gray-400 text-[10px]"></i>
              <span>Cancelamento e Reembolsos</span>
            </router-link>
          </li>
          <li>
            <router-link to="/donativos" class="hover:text-primary transition-colors flex items-center gap-1.5">
              <i class="fa-solid fa-hand-holding-heart text-gray-400 text-[10px]"></i>
              <span>Donativos & Contribuições</span>
            </router-link>
          </li>
          <li class="pt-1">
            <a
              href="https://www.livroreclamacoes.pt"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white transition-all border border-white/10 text-[11px]"
              title="Acesso ao Livro de Reclamações Eletrónico"
            >
              <i class="fa-solid fa-book-open text-primary"></i>
              <span>Livro de Reclamações</span>
              <i class="fa-solid fa-arrow-up-right-from-square text-[9px] text-gray-400"></i>
            </a>
          </li>
        </ul>
      </div>

      <!-- Coluna 4: Pagamentos Seguros & Certificados -->
      <div class="space-y-3">
        <h3 class="text-white font-bold text-sm uppercase tracking-wider">Pagamentos Seguros</h3>
        <p class="text-xs text-gray-400 leading-relaxed">
          Disponibilizamos métodos de pagamento eletrónico auditados e seguros:
        </p>
        
        <!-- Badges de Pagamento -->
        <div class="flex flex-wrap items-center gap-2 pt-1">
          <!-- MB WAY Badge -->
          <div class="bg-white px-2.5 py-1 rounded-lg flex items-center justify-center shadow-sm">
            <MbwayLogo height="18px" />
          </div>
          <!-- SEPA Transfer Badge -->
          <div class="bg-white/10 border border-white/15 px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 text-xs text-white font-semibold">
            <i class="fa-solid fa-building-columns text-white"></i>
            <span>SEPA</span>
          </div>
        </div>

        <!-- Selo de Segurança SSL -->
        <div class="pt-2 flex items-center gap-2 text-[11px] text-emerald-400">
          <i class="fa-solid fa-lock text-xs"></i>
          <span>Ligação Segura SSL/TLS</span>
        </div>
      </div>

    </div>

    <!-- Barra Inferior de Direitos de Autor -->
    <div class="max-w-7xl mx-auto pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-400 gap-3">
      <p>&copy; {{ copyrightText }} — Todos os direitos reservados.</p>
      <p class="text-[11px] text-gray-400">
        Entidade Religiosa e Comunitária sem Fins Lucrativos
      </p>
    </div>
  </footer>
</template>

<script setup>
import logoWhite from '../assets/logo_provisory_white.png'
import MbwayLogo from './icons/MbwayLogo.vue'

const siteOwner = 'Igreja Cristã Manancial de Águas Vivas (ICMAV)'
const nipc = '592 002 403'
const currentYear = new Date().getFullYear()
const copyrightText = `${currentYear} ${siteOwner} NIPC: ${nipc}`
</script>

<style scoped>
</style>