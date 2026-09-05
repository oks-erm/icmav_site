<!-- frontend/src/components/admin/AdminSectionSibs.vue -->
<template>
  <AdminSectionWrapper
    title="Gateway de Pagamentos SIBS"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <div class="sibs-admin-container">
      <div class="info-banner">
        <i class="fa-solid fa-shield-halved text-indigo-500 text-lg flex-shrink-0 mt-0.5"></i>
        <div class="text-xs sm:text-sm text-gray-600 space-y-1">
          <p class="font-bold text-gray-800">Configuração dos acessos à Gateway SIBS (MB WAY)</p>
          <p>
            Introduz as credenciais fornecidas pela SIBS para processar pagamentos por MB WAY na plataforma. Por motivos de segurança, estes campos não possuem valores padrão.
          </p>
        </div>
      </div>

      <div class="grid-1">
        <div class="form-group">
          <label for="sibsApiBase">Endpoint Base da API SIBS</label>
          <input
            id="sibsApiBase"
            v-model="sibsData.sibs_api_base"
            type="text"
            placeholder="Ex: https://spg.qly.site1.sibs.pt/api/v2 (ou endpoint de produção)"
          />
        </div>
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
  </AdminSectionWrapper>
</template>

<script setup>
import { ref } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const sibsData = defineModel({
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
</script>

<style scoped>
.sibs-admin-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.info-banner {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.grid-1 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #4b5563;
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

input {
  font: inherit;
  padding: 0.6rem 0.8rem;
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
</style>
