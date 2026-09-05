<!-- frontend/src/components/admin/AdminSectionLocalGatheringOptions.vue -->
<template>
  <AdminSectionWrapper
    title="Pequenos Grupos"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <template #actions>
      <button type="button" @click.stop="addOptionRow">+ Adicionar linha</button>
    </template>

    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>Slug</th>
            <th>Líder</th>
            <th>Email de contacto</th>
            <th>Tag</th>
            <th>Localidade</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(option, index) in localGatheringOptions" :key="index">
            <td><input v-model="option.slug" type="text" placeholder="pg-carcavelos-casais" /></td>
            <td><input v-model="option.leaderName" type="text" /></td>
            <td><input v-model="option.emailContact" type="email" /></td>
            <td><input v-model="option.characteristicTag" type="text" placeholder="Casais" /></td>
            <td><input v-model="option.location" type="text" /></td>
            <td>
              <button type="button" class="danger-btn" @click="removeOptionRow(index)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'

const localGatheringOptions = defineModel({ type: Array, default: () => [] })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])

function addOptionRow() {
  localGatheringOptions.value.push({
    slug: '',
    leaderName: '',
    emailContact: '',
    characteristicTag: '',
    location: '',
  })
}

function removeOptionRow(index) {
  localGatheringOptions.value.splice(index, 1)
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

.data-table input:focus {
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
