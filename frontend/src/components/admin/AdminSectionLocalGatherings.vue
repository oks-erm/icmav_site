<!-- frontend/src/components/admin/AdminSectionLocalGatherings.vue -->
<template>
  <AdminSectionWrapper
    title="Encontros Locais – Conteúdo"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <div class="field-container">
      <div class="form-group">
        <label for="lgQuote">Citação</label>
        <input id="lgQuote" v-model="localGatheringsData.localGatheringsQuote" type="text" placeholder="Ex: Citação bíblica..." />
      </div>

      <div class="form-group">
        <label for="lgQuoteRef">Autor da citação</label>
        <input id="lgQuoteRef" v-model="localGatheringsData.localGatheringsQuoteReference" type="text" placeholder="Ex: Hebreus 10:24-25" />
      </div>

      <div class="form-group pb-2">
        <label for="lgBody">Corpo do texto</label>
        <RichTextEditor id="lgBody" v-model="localGatheringsData.localGatheringsBody" />
      </div>
    </div>
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import RichTextEditor from '../RichTextEditor.vue'

const localGatheringsData = defineModel({
  type: Object,
  default: () => ({
    localGatheringsQuote: '',
    localGatheringsQuoteReference: '',
    localGatheringsBody: '',
  }),
})

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])
</script>

<style scoped>
.field-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.85rem;
}

input {
  font: inherit;
  padding: 0.7rem 0.9rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  width: 100%;
  background: #fafafa;
  transition: border-color 0.15s;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: #fff;
}
</style>
