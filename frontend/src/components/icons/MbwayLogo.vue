<template>
  <img
    :src="mbwayLogoSvg"
    alt="MB WAY"
    :class="className"
    :style="{ height: height, width: width }"
  />
</template>

<script setup>
import mbwayLogoSvg from '../../assets/MBWAY_H_Positivo.svg'

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
