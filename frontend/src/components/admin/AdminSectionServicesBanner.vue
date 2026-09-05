<!-- frontend/src/components/admin/AdminSectionServicesBanner.vue -->
<template>
  <AdminSectionWrapper
    title="Serviços Banner"
    :is-open="isOpen"
    @toggle="$emit('toggle')"
    @reset="$emit('reset')"
  >
    <RichTextEditor id="servicesBannerContent" v-model="modelValue" />
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
