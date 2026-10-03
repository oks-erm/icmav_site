<!-- frontend/src/components/admin/AdminSectionSocialMedia.vue -->
<template>
  <AdminSectionWrapper
    title="Redes Sociais"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addRow">+ Adicionar linha</button>
    </template>

    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Ícone (classe CSS)</th>
            <th>Preview</th>
            <th>Link</th>
            <th>Cor hover</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in socialMedia" :key="index">
            <td><input v-model="item.icon" type="text" placeholder="fa-brands fa-facebook-f" /></td>
            <td>
              <div class="icon-preview-box">
                <i v-if="item.icon" :class="item.icon"></i>
                <span v-else class="preview-placeholder">—</span>
              </div>
            </td>
            <td><input v-model="item.link" type="url" placeholder="https://…" /></td>
            <td>
              <div class="color-cell">
                <input v-model="item.hoverColor" type="color" class="color-picker" />
                <input v-model="item.hoverColor" type="text" class="color-text" placeholder="#rrggbb" />
              </div>
            </td>
            <td>
              <button type="button" class="danger-btn" @click="removeRow(index)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const socialMedia = defineModel({ type: Array, default: () => [] })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])

function addRow() {
  socialMedia.value.push({
    icon: '',
    link: '',
    hoverColor: '#000000',
  })
}

function removeRow(index) {
  socialMedia.value.splice(index, 1)
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

.data-table input {
  width: 100%;
  min-width: 100px;
  font: inherit;
  padding: 0.5rem 0.7rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background: #fafafa;
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

.color-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.color-picker {
  width: 40px;
  height: 38px;
  padding: 2px;
  border-radius: 6px;
  cursor: pointer;
  flex-shrink: 0;
}

.color-text {
  flex: 1;
  min-width: 80px;
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
