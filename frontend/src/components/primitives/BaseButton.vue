<script setup>
/**
 * Propiedades admitidas por BaseButton.
 *
 * Attributes:
 *   type (string, optional): Tipo HTML del boton.
 *   variants (string, optional): Variante visual aplicada en la clase CSS.
 *   disabled (boolean, optional): Indica si el boton esta deshabilitado.
 *   loading (boolean, optional): Muestra estado de carga y bloquea interaccion.
 */
const props = defineProps({
    type: {
        type: String,
        default: 'button',
    },
    variants: {
        type: String,
        default: 'primary',
    },
    disabled: Boolean,
    loading: Boolean,
})

</script>

<template>
  <button
    :type="props.type"
    :disabled="props.disabled || props.loading"
    :class="[
      'btn',
      `btn-${props.variants}`,
      { 'opacity-50': props.loading }
    ]"
  >
    <span v-if="props.loading" class="spinner-border spinner-border-sm me-2"></span>
    <slot></slot>
  </button>

</template>

