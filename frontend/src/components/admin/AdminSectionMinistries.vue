<!-- frontend/src/components/admin/AdminSectionMinistries.vue -->
<template>
  <AdminSectionWrapper
    title="Ministérios"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addMinistryRow">+ Adicionar ministério</button>
    </template>

    <div class="ministries-container">
      <div
        v-for="(ministry, index) in ministries"
        :key="ministry.slug || index"
        class="ministry-card"
      >
        <!-- Cabeçalho do Card (Acordeão) -->
        <div class="ministry-header" @click="toggleCard(index)">
          <div class="header-left">
            <span class="ministry-icon-badge" :class="ministry.bgClass || 'bg-primary'">
              <i :class="ministry.icon || 'fa-solid fa-church'"></i>
            </span>
            <div>
              <h3 class="ministry-title">{{ ministry.name || 'Novo Ministério' }}</h3>
              <span class="ministry-slug">/ministerios/{{ ministry.slug || 'slug' }}</span>
            </div>
          </div>

          <div class="header-right" @click.stop>
            <button
              type="button"
              class="expand-btn"
              @click="toggleCard(index)"
            >
              {{ openCards[index] ? 'Recolher ▲' : 'Editar Detalhes ▼' }}
            </button>
            <button
              type="button"
              class="danger-btn"
              @click="removeMinistryRow(index)"
            >
              Remover
            </button>
          </div>
        </div>

        <!-- Conteúdo do Card (quando expandido) -->
        <div v-show="openCards[index]" class="ministry-body">
          <!-- 1. DADOS DA HOME -->
          <div class="form-section">
            <h4 class="section-title">
              <i class="fa-solid fa-home text-indigo-500 mr-1"></i> Apresentação na Página Inicial
            </h4>

            <div class="grid-2">
              <div class="form-group">
                <label>Nome do Ministério</label>
                <input v-model="ministry.name" type="text" placeholder="Ex: Mulheres" />
              </div>
              <div class="form-group">
                <label>Identificador URL (Slug)</label>
                <input v-model="ministry.slug" type="text" placeholder="Ex: mulheres" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label>Ícone FontAwesome</label>
                <div class="input-with-preview">
                  <input v-model="ministry.icon" type="text" placeholder="fas fa-female" />
                  <div class="icon-preview-mini">
                    <i v-if="ministry.icon" :class="ministry.icon"></i>
                    <span v-else>—</span>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>Classe de Cor (Tailwind / DaisyUI)</label>
                <input v-model="ministry.bgClass" type="text" placeholder="Ex: bg-info, bg-warning, bg-primary" />
              </div>
            </div>

            <div class="form-group">
              <label>Descrição Curta (Cartão da Home)</label>
              <textarea v-model="ministry.desc" rows="2" placeholder="Resumo de 1-2 frases para o cartão da página inicial..."></textarea>
            </div>
          </div>

          <!-- 2. TEXTO DESCRITIVO DETALHADO -->
          <div class="form-section">
            <h4 class="section-title">
              <i class="fa-solid fa-align-left text-indigo-500 mr-1"></i> Descrição Completa (Página de Detalhes)
            </h4>
            <div class="form-group">
              <label>Texto descritivo (separa parágrafos com uma linha em branco)</label>
              <textarea
                :value="formatLongDescription(ministry.longDescription)"
                @input="updateLongDescription(index, $event.target.value)"
                rows="5"
                placeholder="Insere os parágrafos de apresentação detalhada do ministério..."
              ></textarea>
            </div>
          </div>

          <!-- 3. LIDERANÇA DO MINISTÉRIO -->
          <div class="form-section">
            <h4 class="section-title">
              <i class="fa-solid fa-user-tie text-indigo-500 mr-1"></i> Líder do Ministério
            </h4>

            <div class="grid-2">
              <div class="form-group">
                <label>Nome do Líder</label>
                <input v-model="ministry.leader" type="text" placeholder="Ex: Cristina Silva" />
              </div>
              <div class="form-group">
                <label>Contacto Telefónico ou Email</label>
                <input v-model="ministry.contact" type="text" placeholder="Ex: +351 912 000 555" />
              </div>
            </div>

            <div class="form-group">
              <label>Foto do Líder</label>
              <div class="media-upload-row">
                <input v-model="ministry.leaderPhoto" type="text" placeholder="URL ou ficheiro enviado..." />
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  class="hidden-file-input"
                  :ref="el => setLeaderPhotoInputRef(el, index)"
                  @change="handleLeaderPhotoSelected($event, index)"
                />
                <button
                  type="button"
                  class="secondary-btn"
                  @click="triggerLeaderPhotoUpload(index)"
                  :disabled="uploadingLeaderIndex === index"
                >
                  {{ uploadingLeaderIndex === index ? 'A carregar…' : 'Carregar Foto' }}
                </button>
                <img
                  v-if="ministry.leaderPhoto"
                  :src="getMediaSrc(ministry.leaderPhoto)"
                  :alt="ministry.leader || 'Líder'"
                  class="photo-preview-circle"
                />
              </div>
            </div>
          </div>

          <!-- 4. CONTEÚDO MULTIMÉDIA (FOTO OU VÍDEO) -->
          <div class="form-section">
            <h4 class="section-title">
              <i class="fa-solid fa-photo-film text-indigo-500 mr-1"></i> Conteúdo Multimédia (Foto ou Vídeo)
            </h4>

            <div class="grid-2">
              <div class="form-group">
                <label>Tipo de Multimédia</label>
                <select
                  :value="ministry.media?.type || 'image'"
                  @change="setMediaType(index, $event.target.value)"
                  class="styled-select"
                >
                  <option value="image">Fotografia (Imagem)</option>
                  <option value="video">Pequeno Vídeo (MP4 / WebM)</option>
                </select>
              </div>

              <div class="form-group">
                <label>Ficheiro Multimédia (Upload ou URL)</label>
                <div class="media-upload-row">
                  <input
                    :value="ministry.media?.src || ''"
                    @input="setMediaSrc(index, $event.target.value)"
                    type="text"
                    placeholder="/uploads/ministries/... ou URL"
                  />
                  <input
                    type="file"
                    accept="image/png,image/jpeg,image/webp,video/mp4,video/webm"
                    class="hidden-file-input"
                    :ref="el => setMediaFileInputRef(el, index)"
                    @change="handleMediaSelected($event, index)"
                  />
                  <button
                    type="button"
                    class="secondary-btn"
                    @click="triggerMediaUpload(index)"
                    :disabled="uploadingMediaIndex === index"
                  >
                    {{ uploadingMediaIndex === index ? 'A carregar…' : 'Upload Ficheiro' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Preview Multimédia -->
            <div v-if="ministry.media?.src" class="media-preview-box">
              <video
                v-if="ministry.media?.type === 'video'"
                :src="getMediaSrc(ministry.media.src)"
                controls
                muted
                class="video-preview"
              >
                Vídeo não suportado.
              </video>
              <img
                v-else
                :src="getMediaSrc(ministry.media.src)"
                :alt="ministry.name"
                class="image-preview"
              />
            </div>
          </div>

          <!-- 5. REDES SOCIAIS -->
          <div class="form-section">
            <h4 class="section-title">
              <i class="fa-brands fa-instagram text-indigo-500 mr-1"></i> Redes Sociais do Ministério
            </h4>
            <div class="form-group">
              <label>Link Instagram do Ministério</label>
              <input
                :value="getInstagramLink(ministry)"
                @input="setInstagramLink(index, $event.target.value)"
                type="text"
                placeholder="https://instagram.com/..."
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import { ref, onBeforeUpdate } from 'vue'
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import { uploadMinistryLeaderPhoto, uploadMinistryMedia } from '../../services/api'

const BACKEND_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const ministries = defineModel({ type: Array, default: () => [] })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle', 'reset', 'notify'])

// Gestão de cartões abertos (acordeão)
const openCards = ref({})
function toggleCard(index) {
  openCards.value[index] = !openCards.value[index]
}

// Helpers para formatos multimédia
function getMediaSrc(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('/uploads/')) return `${BACKEND_BASE}${path}`
  return path
}

// Helpers para Descrição Longa
function formatLongDescription(val) {
  if (Array.isArray(val)) return val.join('\n\n')
  return val || ''
}

function updateLongDescription(index, text) {
  const paragraphs = text.split('\n\n').map(p => p.trim()).filter(Boolean)
  ministries.value[index].longDescription = paragraphs
}

// Helpers para Media
function setMediaType(index, type) {
  if (!ministries.value[index].media) {
    ministries.value[index].media = { type: 'image', src: '', placeholder: '' }
  }
  ministries.value[index].media.type = type
}

function setMediaSrc(index, src) {
  if (!ministries.value[index].media) {
    ministries.value[index].media = { type: 'image', src: '', placeholder: '' }
  }
  ministries.value[index].media.src = src
}

// Helpers para Redes Sociais
function getInstagramLink(m) {
  if (Array.isArray(m.socialMedia) && m.socialMedia.length) {
    return m.socialMedia[0].link || ''
  }
  return ''
}

function setInstagramLink(index, link) {
  if (!Array.isArray(ministries.value[index].socialMedia)) {
    ministries.value[index].socialMedia = []
  }
  if (link.trim()) {
    ministries.value[index].socialMedia = [{ icon: 'fab fa-instagram', link: link.trim() }]
  } else {
    ministries.value[index].socialMedia = []
  }
}

// Upload Foto Líder
const leaderPhotoInputs = ref([])
const uploadingLeaderIndex = ref(null)

function setLeaderPhotoInputRef(el, index) {
  if (el) leaderPhotoInputs.value[index] = el
}

function triggerLeaderPhotoUpload(index) {
  leaderPhotoInputs.value[index]?.click()
}

async function handleLeaderPhotoSelected(event, index) {
  const file = event.target.files?.[0]
  if (!file) return

  uploadingLeaderIndex.value = index
  try {
    const data = await uploadMinistryLeaderPhoto(file)
    ministries.value[index].leaderPhoto = data.url
    emit('notify', { type: 'success', message: 'Foto do líder carregada com sucesso.' })
  } catch (err) {
    emit('notify', { type: 'error', message: err.message || 'Erro ao carregar foto.' })
  } finally {
    uploadingLeaderIndex.value = null
    event.target.value = ''
  }
}

// Upload Multimédia (Imagem ou Vídeo)
const mediaFileInputs = ref([])
const uploadingMediaIndex = ref(null)

function setMediaFileInputRef(el, index) {
  if (el) mediaFileInputs.value[index] = el
}

function triggerMediaUpload(index) {
  mediaFileInputs.value[index]?.click()
}

async function handleMediaSelected(event, index) {
  const file = event.target.files?.[0]
  if (!file) return

  uploadingMediaIndex.value = index
  try {
    const data = await uploadMinistryMedia(file)
    if (!ministries.value[index].media) {
      ministries.value[index].media = { type: 'image', src: '', placeholder: '' }
    }
    ministries.value[index].media.src = data.url
    if (data.mediaType) {
      ministries.value[index].media.type = data.mediaType
    }
    emit('notify', { type: 'success', message: 'Conteúdo multimédia carregado com sucesso.' })
  } catch (err) {
    emit('notify', { type: 'error', message: err.message || 'Erro ao carregar multimédia.' })
  } finally {
    uploadingMediaIndex.value = null
    event.target.value = ''
  }
}

onBeforeUpdate(() => {
  leaderPhotoInputs.value = []
  mediaFileInputs.value = []
})

function addMinistryRow() {
  const newIndex = ministries.value.length
  ministries.value.push({
    name: 'Novo Ministério',
    slug: 'novo-ministerio',
    icon: 'fa-solid fa-church',
    bgClass: 'bg-primary',
    desc: '',
    longDescription: [],
    leader: '',
    leaderPhoto: '',
    contact: '',
    media: {
      type: 'image',
      src: '',
      placeholder: ''
    },
    socialMedia: []
  })
  openCards.value[newIndex] = true
}

function removeMinistryRow(index) {
  if (confirm(`Tens a certeza que desejas remover o ministério "${ministries.value[index]?.name || ''}"?`)) {
    ministries.value.splice(index, 1)
  }
}
</script>

<style scoped>
.ministries-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0.5rem;
}

.ministry-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.ministry-header {
  padding: 1rem 1.25rem;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid transparent;
  transition: background 0.15s;
}

.ministry-header:hover {
  background: #f3f4f6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ministry-icon-badge {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.ministry-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #111827;
}

.ministry-slug {
  font-size: 0.8rem;
  color: #6b7280;
  font-family: monospace;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.expand-btn {
  background: #eef2ff;
  color: #4f46e5;
  font-size: 0.82rem;
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
}

.ministry-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #fff;
}

.form-section {
  background: #fbfbfb;
  border: 1px solid #f0f0f0;
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
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

.form-group input,
.form-group textarea,
.styled-select {
  font: inherit;
  padding: 0.55rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: #fff;
  font-size: 0.875rem;
}

.form-group input:focus,
.form-group textarea:focus,
.styled-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.input-with-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.input-with-preview input {
  flex-grow: 1;
}

.icon-preview-mini {
  width: 38px;
  height: 38px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  color: #4b5563;
  flex-shrink: 0;
}

.media-upload-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.media-upload-row input {
  flex-grow: 1;
}

.hidden-file-input {
  display: none;
}

.photo-preview-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-cover: cover;
  border: 2px solid #e0e7ff;
  flex-shrink: 0;
}

.media-preview-box {
  margin-top: 0.5rem;
  max-width: 320px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  background: #000;
}

.video-preview,
.image-preview {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  display: block;
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

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.secondary-btn {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.danger-btn {
  background: #fee4e2;
  color: #b42318;
}
</style>
