<!-- frontend/src/components/admin/AdminSectionDonations.vue -->
<template>
  <AdminSectionWrapper
    title="Contribuições"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <div class="donations-admin-container">
      
      <!-- 1. APRESENTAÇÃO NA PÁGINA INICIAL -->
      <div class="admin-subcard">
        <h4 class="subcard-title">
          <i class="fa-solid fa-home text-indigo-500 mr-1.5"></i> 1. Apresentação na Página Inicial
        </h4>
        
        <div class="subcard-content">
          <div class="form-group">
            <label for="donationsBody">Texto Principal</label>
            <RichTextEditor id="donationsBody" v-model="donationsData.donationsBody" />
          </div>

          <div class="grid-2 mt-3">
            <div class="form-group">
              <label for="donationsQuote">Citação Bíblica</label>
              <input
                id="donationsQuote"
                v-model="donationsData.donationsQuote"
                type="text"
                placeholder="Ex: Cada um dê conforme determinou no seu coração..."
              />
            </div>
            <div class="form-group">
              <label for="donationsQuoteRef">Referência Bíblica</label>
              <input
                id="donationsQuoteRef"
                v-model="donationsData.donationsQuoteAuthor"
                type="text"
                placeholder="Ex: 2 Coríntios 9:7"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 2. CATEGORIAS DE CONTRIBUIÇÃO (DROPDOWN) -->
      <div class="admin-subcard">
        <div class="flex items-center justify-between mb-2">
          <h4 class="subcard-title border-none mb-0 pb-0">
            <i class="fa-solid fa-list-check text-indigo-500 mr-1.5"></i> 2. Categorias de Contribuição (Dropdown)
          </h4>
          <button type="button" class="add-cat-btn" @click="addCategoryRow">
            + Adicionar Categoria
          </button>
        </div>

        <p class="text-xs text-gray-500 mb-3">
          Define as categorias que surgem na dropdown do formulário de contribuição (ex: Ofertas, Dízimos, Missões).
        </p>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nome da Categoria</th>
                <th style="width: 90px; text-align: center;">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(cat, index) in safeCategories" :key="index">
                <td>
                  <input
                    v-model="cat.name"
                    type="text"
                    placeholder="Ex: Ofertas, Dízimos, Missões..."
                    @input="syncCategoryId(index)"
                  />
                </td>
                <td style="text-align: center;">
                  <button
                    type="button"
                    class="danger-btn"
                    @click="removeCategoryRow(index)"
                    :disabled="safeCategories.length <= 1"
                  >
                    Remover
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 3. DADOS PARA TRANSFERÊNCIA BANCÁRIA -->
      <div class="admin-subcard">
        <h4 class="subcard-title">
          <i class="fa-solid fa-building-columns text-indigo-500 mr-1.5"></i> 3. Dados para Transferência Bancária
        </h4>
        
        <div class="subcard-content">
          <div class="grid-2">
            <div class="form-group">
              <label>Beneficiário / Titular da Conta</label>
              <input v-model="donationsData.beneficiary" type="text" placeholder="Igreja Cristã Manancial de Águas Vivas" />
            </div>
            <div class="form-group">
              <label>IBAN</label>
              <input v-model="donationsData.iban" type="text" placeholder="PT50 0007 0246 0014 0750 0033 4" />
            </div>
          </div>

          <div class="grid-3">
            <div class="form-group">
              <label>Banco</label>
              <input v-model="donationsData.bank" type="text" placeholder="NOVO BANCO, SA" />
            </div>
            <div class="form-group">
              <label>BIC / SWIFT</label>
              <input v-model="donationsData.bic" type="text" placeholder="BESCPTPLXXX" />
            </div>
            <div class="form-group">
              <label>Email para Envio de Comprovativos</label>
              <input v-model="donationsData.treasuryEmail" type="email" placeholder="tesouraria.icmav@gmail.com" />
            </div>
          </div>
        </div>
      </div>

      <!-- 4. GATEWAY DE PAGAMENTOS SIBS -->
      <div class="admin-subcard">
        <h4 class="subcard-title">
          <i class="fa-solid fa-shield-halved text-indigo-500 mr-1.5"></i> 4. Gateway de Pagamentos SIBS (MB WAY)
        </h4>

        <div class="info-banner mb-3">
          <i class="fa-solid fa-circle-info text-indigo-500 text-sm flex-shrink-0 mt-0.5"></i>
          <span class="text-xs text-gray-600">
            Credenciais para emissão e processamento de donativos por MB WAY através da Gateway SIBS. Sem valores pré-definidos por segurança.
          </span>
        </div>

        <div class="subcard-content">
          <div class="form-group">
            <label for="sibsApiBase">Endpoint Base da API SIBS</label>
            <input
              id="sibsApiBase"
              v-model="sibsData.sibs_api_base"
              type="text"
              placeholder="Ex: https://spg.qly.site1.sibs.pt/api/v2 (ou endpoint de produção)"
            />
          </div>

          <div class="grid-2">
            <div class="form-group">
              <label for="sibsClientId">Client ID (X-IBM-Client-Id)</label>
              <input
                id="sibsClientId"
                v-model="sibsData.sibs_client_id"
                type="text"
                placeholder="Introduz o Client ID"
              />
            </div>

            <div class="form-group">
              <label for="sibsTerminalId">Terminal ID</label>
              <input
                id="sibsTerminalId"
                v-model="sibsData.sibs_terminal_id"
                type="text"
                placeholder="Ex: 12345"
              />
            </div>
          </div>

          <div class="grid-2">
            <div class="form-group">
              <div class="label-with-action">
                <label for="sibsBearerToken">Bearer Token de Autorização</label>
                <button
                  type="button"
                  class="text-link"
                  @click="showBearerToken = !showBearerToken"
                >
                  {{ showBearerToken ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
              <input
                id="sibsBearerToken"
                v-model="sibsData.sibs_bearer_token"
                :type="showBearerToken ? 'text' : 'password'"
                placeholder="Introduz o Bearer Token"
              />
            </div>

            <div class="form-group">
              <div class="label-with-action">
                <label for="sibsClientSecret">Client Secret</label>
                <button
                  type="button"
                  class="text-link"
                  @click="showClientSecret = !showClientSecret"
                >
                  {{ showClientSecret ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
              <input
                id="sibsClientSecret"
                v-model="sibsData.sibs_client_secret"
                :type="showClientSecret ? 'text' : 'password'"
                placeholder="Introduz o Client Secret"
              />
            </div>
          </div>
        </div>
      </div>

    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import { ref, computed } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import RichTextEditor from '../RichTextEditor.vue'

const donationsData = defineModel({
  type: Object,
  default: () => ({
    donationsBody: '',
    donationsQuote: '',
    donationsQuoteAuthor: '',
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
  }),
})

const sibsData = defineModel('sibs', {
  type: Object,
  default: () => ({
    sibs_api_base: '',
    sibs_bearer_token: '',
    sibs_client_id: '',
    sibs_client_secret: '',
    sibs_terminal_id: '',
  }),
})

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])

const showBearerToken = ref(false)
const showClientSecret = ref(false)

const safeCategories = computed(() => {
  if (Array.isArray(donationsData.value?.categories)) {
    return donationsData.value.categories
  }
  return []
})

function syncCategoryId(index) {
  if (donationsData.value.categories[index]) {
    donationsData.value.categories[index].id = donationsData.value.categories[index].name
  }
}

function addCategoryRow() {
  if (!Array.isArray(donationsData.value.categories)) {
    donationsData.value.categories = []
  }
  donationsData.value.categories.push({
    id: 'Nova Categoria',
    name: 'Nova Categoria',
  })
}

function removeCategoryRow(index) {
  if (Array.isArray(donationsData.value.categories)) {
    donationsData.value.categories.splice(index, 1)
  }
}
</script>

<style scoped>
.donations-admin-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.admin-subcard {
  background: #fbfbfb;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.subcard-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.6rem;
}

.subcard-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-weight: 600;
  color: #4b5563;
  font-size: 0.82rem;
}

.label-with-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.text-link {
  background: transparent;
  border: none;
  color: #6366f1;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}

.text-link:hover {
  text-decoration: underline;
}

.info-banner {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
  }
}

input {
  font: inherit;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  width: 100%;
  background: #fff;
  font-size: 0.875rem;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.data-table th,
.data-table td {
  border: 1px solid #e5e7eb;
  padding: 0.6rem 0.75rem;
  vertical-align: middle;
  text-align: left;
}

.data-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.add-cat-btn {
  background: #6366f1;
  color: #fff;
  font-weight: 600;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-size: 0.82rem;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s;
}

.add-cat-btn:hover {
  opacity: 0.9;
}

.danger-btn {
  background: #fee4e2;
  color: #b42318;
  font-weight: 600;
  padding: 0.4rem 0.65rem;
  border-radius: 6px;
  font-size: 0.8rem;
  border: none;
  cursor: pointer;
}

.danger-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
