<template>
  <img
    :src="sepaLogoSvg"
    alt="SEPA"
    :class="className"
    :style="{ height: height, width: width }"
  />
</template>

<script setup>
import sepaLogoSvg from '../../assets/sepa.svg'

defineProps({
  className: {
    type: String,
    default: 'inline-block align-middle object-contain'
  },
  height: {
    type: String,
    default: '24px'
  },
  width: {
    type: String,
    default: 'auto'
  }
})
</script>
