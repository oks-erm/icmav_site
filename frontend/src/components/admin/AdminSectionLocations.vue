<!-- frontend/src/components/admin/AdminSectionLocations.vue -->
<template>
  <AdminSectionWrapper
    title="Localizações"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addLocationRow">+ Adicionar localização</button>
    </template>

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
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const locations = defineModel({ type: Array, default: () => [] })

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
.locations-list {
  display: grid;
  gap: 1rem;
  margin-top: 0.25rem;
}

.location-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
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

button {
  cursor: pointer;
  border: none;
  background: #6366f1;
  color: #fff;
  font-weight: 600;
  white-space: nowrap;
  padding: 0.5rem 0.85rem;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: opacity 0.15s;
}

button:hover:not(:disabled) {
  opacity: 0.85;
}

.danger-btn {
  background: #fee4e2;
  color: #b42318;
}
</style>
