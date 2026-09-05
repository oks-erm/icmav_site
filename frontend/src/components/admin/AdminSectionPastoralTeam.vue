<!-- frontend/src/components/admin/AdminSectionPastoralTeam.vue -->
<template>
  <AdminSectionWrapper
    title="Equipa pastoral"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addPastorRow">+ Adicionar linha</button>
    </template>

    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Foto</th>
            <th>Bio</th>
            <th>Spouse ID</th>
            <th>Casal principal</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(pastor, index) in pastoralTeam" :key="pastor.id">
            <td style="min-width:60px">
              <input v-model.number="pastor.id" type="number" />
            </td>
            <td style="min-width:140px">
              <textarea v-model="pastor.name" rows="2"></textarea>
            </td>
            <td>
              <div class="photo-cell">
                <input v-model="pastor.photo" type="text" placeholder="/uploads/pastoral_team/foto.jpg" />
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  class="hidden-file-input"
                  :ref="el => setPastorFileInputRef(el, index)"
                  @change="handlePhotoSelected($event, index)"
                />
                <button type="button" class="secondary-btn" @click="triggerPhotoUpload(index)">
                  Upload foto
                </button>
                <img
                  v-if="pastor.photo"
                  :src="getImageSrc(pastor.photo)"
                  :alt="pastor.name || 'Foto pastoral'"
                  class="photo-preview"
                />
              </div>
            </td>
            <td style="min-width:260px">
              <RichTextEditor v-model="pastor.bio" />
            </td>
            <td style="min-width:80px">
              <input
                :value="pastor.spouseId ?? ''"
                type="number"
                @input="pastor.spouseId = $event.target.value === '' ? null : Number($event.target.value)"
              />
            </td>
            <td>
              <label class="checkbox-cell">
                <input v-model="pastor.isLeadPair" type="checkbox" />
                <span>Principal</span>
              </label>
            </td>
            <td>
              <button type="button" class="danger-btn" @click="removePastorRow(index)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import { ref, onBeforeUpdate } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import RichTextEditor from '../RichTextEditor.vue'
import { uploadPastoralTeamPhoto } from '../../services/api'

const pastoralTeam = defineModel({ type: Array, default: () => [] })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle', 'reset', 'notify'])

const BACKEND_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api').replace(/\/api$/, '')

function getImageSrc(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('/uploads/')) return `${BACKEND_BASE}${path}`
  return path
}

const pastorFileInputs = ref([])
onBeforeUpdate(() => {
  pastorFileInputs.value = []
})

function setPastorFileInputRef(el, index) {
  if (el) pastorFileInputs.value[index] = el
}

function triggerPhotoUpload(index) {
  pastorFileInputs.value[index]?.click()
}

async function handlePhotoSelected(event, index) {
  const file = event.target.files?.[0]
  if (!file) return

  try {
    const data = await uploadPastoralTeamPhoto(file)
    pastoralTeam.value[index].photo = data.url
    emit('notify', { type: 'success', message: 'Foto carregada com sucesso.' })
  } catch (err) {
    emit('notify', { type: 'error', message: err.message || 'Erro ao carregar foto.' })
  } finally {
    event.target.value = ''
  }
}

function addPastorRow() {
  pastoralTeam.value.push({
    id: Date.now(),
    name: '',
    photo: '',
    bio: '',
    spouseId: null,
    isLeadPair: false,
  })
}

function removePastorRow(index) {
  pastoralTeam.value.splice(index, 1)
}
</script>

<style scoped>
.table-wrapper {
  overflow-x: auto;
  margin-top: 0.25rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
}

.data-table th,
.data-table td {
  border: 1px solid #e5e7eb;
  padding: 0.6rem 0.75rem;
  vertical-align: top;
  text-align: left;
}

.data-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.data-table input,
.data-table textarea {
  width: 100%;
  min-width: 100px;
  font: inherit;
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background: #fafafa;
}

.data-table input:focus,
.data-table textarea:focus {
  outline: none;
  border-color: #6366f1;
  background: #fff;
}

.photo-cell {
  display: grid;
  gap: 0.5rem;
  min-width: 200px;
}

.hidden-file-input {
  display: none;
}

.photo-preview {
  width: 88px;
  height: 88px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background: #f8fafc;
}

.checkbox-cell {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  cursor: pointer;
}

.checkbox-cell input[type="checkbox"] {
  width: auto;
  cursor: pointer;
  accent-color: #6366f1;
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

.secondary-btn {
  background: #eef2ff;
  color: #3730a3;
}

.danger-btn {
  background: #fee4e2;
  color: #b42318;
}
</style>
