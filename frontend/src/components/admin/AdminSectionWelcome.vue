<!-- frontend/src/components/admin/AdminSectionWelcome.vue -->
<template>
  <AdminSectionWrapper
    title="Conteúdo do componente Info (Welcome)"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <RichTextEditor id="infoContent" v-model="modelValue" />
  </AdminSectionWrapper>
</template>

<script setup>
import AdminSectionWrapper from './AdminSectionWrapper.vue'
import RichTextEditor from '../RichTextEditor.vue'

const modelValue = defineModel({ type: String, default: '' })

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle', 'reset'])
</script>
