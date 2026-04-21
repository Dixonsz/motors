<script setup>
/**
 * Eventos emitidos por BaseForm.
 *
 * El formulario emite submit para delegar el manejo al componente padre.
 */
const emit = defineEmits(['submit'])

/**
 * Reemite el evento submit capturado en el formulario.
 *
 * Args:
 *   event (SubmitEvent): Evento nativo de envio del formulario.
 *
 * Returns:
 *   void
 */
const handleSubmit = (event) => {
    emit('submit', event)
}
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <slot></slot>
    </form>
</template>