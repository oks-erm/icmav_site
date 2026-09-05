<!-- frontend/src/components/admin/AdminSectionWrapper.vue -->
<template>
  <div class="section-container">
    <div class="section-header" @click="$emit('toggle')">
      <div class="section-title">
        <i class="fa-solid fa-chevron-down" :class="{ 'rotate-180': isOpen }"></i>
        <span>{{ title }}</span>
      </div>
      <div class="actions" @click.stop>
        <button
          v-if="showReset"
          type="button"
          class="secondary-btn"
          @click="$emit('reset')"
        >
          {{ resetLabel }}
        </button>
        <slot name="actions"></slot>
      </div>
    </div>
    <div v-show="isOpen" class="section-body">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
  showReset: {
    type: Boolean,
    default: true,
  },
  resetLabel: {
    type: String,
    default: 'Reset',
  },
})

defineEmits(['toggle', 'reset'])
</script>

<style scoped>
.section-container {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f9fafb;
  user-select: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.section-header:hover {
  background: #f3f4f6;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-size: 1.05rem;
}

.section-title i {
  transition: transform 0.3s ease;
}

.section-title .rotate-180 {
  transform: rotate(-180deg);
}

.actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.section-body {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
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
</style>
