<!-- frontend/src/components/admin/AdminSectionGallery.vue -->
<template>
  <AdminSectionWrapper
    title="Galeria"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addGalleryImage">+ Adicionar foto</button>
    </template>

    <div class="gallery-grid">
      <div v-for="(img, idx) in galleryImages" :key="idx" class="gallery-item">
        <input v-model="galleryImages[idx]" type="text" placeholder="URL ou caminho da imagem" />
        <div class="gallery-item-actions">
          <button type="button" class="secondary-btn" @click="triggerUpload(idx)">Upload</button>
          <button type="button" class="danger-btn" @click="removeGalleryImage(idx)">Remover</button>
        </div>
        <input
          type="file"
          class="hidden-file-input"
          :ref="el => setGalleryFileInputRef(el, idx)"
          @change="handlePhotoSelected($event, idx)"
          accept="image/jpeg,image/png,image/webp"
        />
        <img
          v-if="galleryImages[idx]"
          :src="getImageSrc(galleryImages[idx])"
          class="photo-preview"
          alt="Pré-visualização"
        />
      </div>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import { ref, onBeforeUpdate } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import { uploadGalleryPhoto } from '../../services/api'

const galleryImages = defineModel({ type: Array, default: () => [] })

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

const galleryFileInputs = ref([])
onBeforeUpdate(() => {
  galleryFileInputs.value = []
})

function setGalleryFileInputRef(el, index) {
  if (el) galleryFileInputs.value[index] = el
}

function triggerUpload(index) {
  galleryFileInputs.value[index]?.click()
}

async function handlePhotoSelected(event, idx) {
  const file = event.target.files?.[0]
  if (!file) return

  try {
    const data = await uploadGalleryPhoto(file)
    galleryImages.value[idx] = data.url
    emit('notify', { type: 'success', message: 'Foto da galeria carregada com sucesso.' })
  } catch (err) {
    emit('notify', { type: 'error', message: err.message || 'Erro ao carregar foto da galeria.' })
  } finally {
    event.target.value = ''
  }
}

function addGalleryImage() {
  galleryImages.value.push('')
}

function removeGalleryImage(idx) {
  galleryImages.value.splice(idx, 1)
}
</script>

<style scoped>
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-top: 0.25rem;
}

.gallery-item {
  display: grid;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f9fafb;
}

.gallery-item-actions {
  display: flex;
  gap: 0.5rem;
}

.hidden-file-input {
  display: none;
}

.photo-preview {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #f8fafc;
}

input {
  font: inherit;
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  width: 100%;
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

.secondary-btn {
  background: #eef2ff;
  color: #3730a3;
}

.danger-btn {
  background: #fee4e2;
  color: #b42318;
}
</style>
