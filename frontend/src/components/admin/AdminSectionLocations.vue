<!-- frontend/src/components/admin/AdminSectionLocations.vue -->
<template>
  <AdminSectionWrapper
    title="Localizações"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <div class="locations-admin-container">
      <!-- 1. CONFIGURAÇÃO GOOGLE MAPS -->
      <div class="admin-subcard">
        <h4 class="subcard-title">
          <i class="fa-solid fa-map-location-dot text-indigo-500 mr-1.5"></i> 1. Configuração da API do Google Maps
        </h4>

        <div class="info-banner">
          <i class="fa-solid fa-circle-info text-indigo-500 text-sm flex-shrink-0 mt-0.5"></i>
          <span class="text-xs text-gray-600">
            A chave de API é utilizada pelo browser para carregar o mapa interativo na secção "Onde estamos".
            Recomenda-se aplicar restrição de <strong>Referenciador HTTP (websites)</strong> na consola Google Cloud (ex: <code>icmav.pt/*</code>).
          </span>
        </div>

        <div class="subcard-content">
          <div class="grid-2">
            <div class="form-group">
              <div class="label-with-action">
                <label for="googleMapsApiKey">Google Maps API Key</label>
                <button
                  type="button"
                  class="text-link"
                  @click="showApiKey = !showApiKey"
                >
                  {{ showApiKey ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>
              <input
                id="googleMapsApiKey"
                v-model="googleMapsData.apiKey"
                :type="showApiKey ? 'text' : 'password'"
                placeholder="AIzaSy..."
                autocomplete="off"
              />
            </div>

            <div class="form-group">
              <label for="googleMapsMapId">Map ID <small class="text-gray-400 font-normal">(Opcional - Estilos / Advanced Markers)</small></label>
              <input
                id="googleMapsMapId"
                v-model="googleMapsData.mapId"
                type="text"
                placeholder="263a0b6477b428b3ae996650"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 2. LISTA DE LOCALIZAÇÕES -->
      <div class="admin-subcard">
        <div class="flex items-center justify-between mb-2">
          <h4 class="subcard-title border-none mb-0 pb-0">
            <i class="fa-solid fa-church text-indigo-500 mr-1.5"></i> 2. Igrejas e Extensões
          </h4>
          <button type="button" class="add-loc-btn" @click.stop="addLocationRow">
            + Adicionar Localização
          </button>
        </div>

        <div class="locations-list">
          <div v-for="(loc, index) in locations" :key="index" class="location-card">
            <div class="location-card-header">
              <strong>{{ loc.name || 'Nova localização' }}</strong>
              <button type="button" class="danger-btn" @click="removeLocationRow(index)">Remover</button>
            </div>
            <div class="location-fields">
              <div class="field-row">
                <label>Slug</label>
                <input v-model="loc.slug" type="text" placeholder="sede" />
              </div>
              <div class="field-row">
                <label>Nome</label>
                <input v-model="loc.name" type="text" />
              </div>
              <div class="field-row">
                <label>Tipo</label>
                <input v-model="loc.type" type="text" placeholder="Sede / Extensão" />
              </div>
              <div class="field-row">
                <label>Email</label>
                <input v-model="loc.email" type="email" />
              </div>
              <div class="field-row">
                <label>Telefone</label>
                <input v-model="loc.phone" type="tel" />
              </div>
              <div class="field-row">
                <label>Morada</label>
                <input v-model="loc.address" type="text" />
              </div>
              <div class="field-row">
                <label>Link Google Maps</label>
                <input v-model="loc.mapsLink" type="url" />
              </div>
              <div class="field-row">
                <label>Website personalizado <small>(opcional)</small></label>
                <input
                  :value="loc.customWebsite ?? ''"
                  type="text"
                  placeholder="ex: icmavlondon.com"
                  @input="loc.customWebsite = $event.target.value.trim() || null"
                />
              </div>
              <div class="field-row">
                <label>Culto dominical</label>
                <input v-model="loc.sundayService" type="text" placeholder="10h30" />
              </div>
              <div class="field-row">
                <label>Posição no mapa <small>(lat,lng)</small></label>
                <input v-model="loc.markerPosition" type="text" placeholder="38.724251,-9.327461" />
              </div>
              <div class="field-row">
                <label>Zoom no mapa <small>(1–21)</small></label>
                <input v-model.number="loc.mapZoom" type="number" min="1" max="21" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import { ref } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const locations = defineModel({ type: Array, default: () => [] })

const googleMapsData = defineModel('googleMaps', {
  type: Object,
  default: () => ({
    apiKey: '',
    mapId: '',
  }),
})

const showApiKey = ref(false)

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])

function addLocationRow() {
  locations.value.push({
    slug: '',
    name: '',
    type: 'Extensão',
    email: '',
    phone: '',
    address: '',
    mapsLink: '',
    customWebsite: null,
    sundayService: '',
    markerPosition: '',
    mapZoom: 17,
  })
}

function removeLocationRow(index) {
  locations.value.splice(index, 1)
}
</script>

<style scoped>
.locations-admin-container {
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

.info-banner {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: #eef2ff;
  border: 1px solid #c7d2fe;
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
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
  font-size: 0.825rem;
  font-weight: 600;
  color: #4b5563;
}

.label-with-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-link {
  background: none;
  border: none;
  color: #6366f1;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}

.add-loc-btn {
  background: #4f46e5;
  color: #ffffff;
  border: none;
  padding: 0.4rem 0.85rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}

.add-loc-btn:hover {
  background: #4338ca;
}

.locations-list {
  display: grid;
  gap: 1rem;
  margin-top: 0.25rem;
}

.location-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
}

.location-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}

.location-fields {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.5rem 1.25rem;
  padding: 1rem;
}

.field-row {
  display: grid;
  gap: 0.2rem;
}

.field-row label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
}

.field-row label small {
  font-weight: 400;
  color: #9ca3af;
}

input {
  font: inherit;
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  width: 100%;
  background: #fafafa;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: #fff;
}

.danger-btn {
  cursor: pointer;
  border: none;
  background: #fee4e2;
  color: #b42318;
  font-weight: 600;
  white-space: nowrap;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  transition: opacity 0.15s;
}

.danger-btn:hover {
  opacity: 0.85;
}
</style>
