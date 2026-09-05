<!-- frontend/src/components/admin/AdminSectionPurposes.vue -->
<template>
  <AdminSectionWrapper
    title="Propósitos"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addPurposeRow">+ Adicionar linha</button>
    </template>

    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Ícone</th>
            <th>Preview</th>
            <th>Cor (bgClass)</th>
            <th>Descrição</th>
            <th>Passagem bíblica</th>
            <th>Referência</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(purpose, index) in purposes" :key="index">
            <td><input v-model="purpose.title" type="text" /></td>
            <td><input v-model="purpose.icon" type="text" placeholder="fas fa-heart" /></td>
            <td>
              <div class="icon-preview-box">
                <i v-if="purpose.icon" :class="purpose.icon"></i>
                <span v-else class="preview-placeholder">—</span>
              </div>
            </td>
            <td><input v-model="purpose.bgClass" type="text" placeholder="bg-primary" /></td>
            <td><textarea v-model="purpose.desc" rows="3"></textarea></td>
            <td><textarea v-model="purpose.biblicalPassage" rows="3"></textarea></td>
            <td><input v-model="purpose.biblicalReference" type="text" /></td>
            <td>
              <button type="button" class="danger-btn" @click="removePurposeRow(index)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const purposes = defineModel({ type: Array, default: () => [] })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])

function addPurposeRow() {
  purposes.value.push({
    title: '',
    icon: '',
    bgClass: '',
    desc: '',
    biblicalPassage: '',
    biblicalReference: '',
  })
}

function removePurposeRow(index) {
  purposes.value.splice(index, 1)
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

.icon-preview-box {
  min-height: 40px;
  min-width: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
  padding: 0.5rem;
}

.icon-preview-box i {
  font-size: 1.3rem;
}

.preview-placeholder {
  color: #98a2b3;
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
