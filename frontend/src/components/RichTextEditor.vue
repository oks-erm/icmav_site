<!-- src/components/RichTextEditor.vue -->
 
<template>
  <div class="rich-text-editor">
    <div ref="editorContainer" class="editor-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const editorContainer = ref(null)
let quill = null
let isUpdating = false

onMounted(() => {
  quill = new Quill(editorContainer.value, {
    theme: 'snow',
    modules: {
      toolbar: [
        [{ 'header': [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['link', 'clean']
      ]
    }
  })

  if (props.modelValue) {
    quill.root.innerHTML = props.modelValue
  }

  quill.on('text-change', (delta, oldDelta, source) => {
    if (source !== 'user') return
    isUpdating = true
    let html = quill.root.innerHTML
    if (html === '<p><br></p>') html = ''
    emit('update:modelValue', html)
    setTimeout(() => { isUpdating = false }, 0)
  })
})

watch(() => props.modelValue, (newValue) => {
  if (!isUpdating && quill) {
    const val = newValue || ''
    if (quill.root.innerHTML !== val) {
      quill.root.innerHTML = val
    }
  }
})

onBeforeUnmount(() => {
  if (quill) {
    quill.off('text-change')
    quill = null
  }
})
</script>

<style scoped>
.rich-text-editor {
  border-radius: 8px;
  background: #fff;
  width: 100%;
}
:deep(.ql-toolbar.ql-snow) {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border-color: #d1d5db;
  background: #fafafa;
  font-family: inherit;
}
:deep(.ql-container.ql-snow) {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  border-color: #d1d5db;
  font-family: inherit;
  font-size: inherit;
  min-height: 150px;
}
:deep(.ql-editor) {
  min-height: 150px;
}
:deep(.ql-editor:focus) {
  outline: none;
}
.rich-text-editor:focus-within :deep(.ql-toolbar.ql-snow),
.rich-text-editor:focus-within :deep(.ql-container.ql-snow) {
  border-color: #6366f1;
}
</style>
