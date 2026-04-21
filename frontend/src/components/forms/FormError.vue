<script setup>
/**
 * Propiedades admitidas por FormError.
 *
 * Attributes:
 *   error (string, optional): Mensaje de error a mostrar bajo el campo.
 */
const props = defineProps({
    error: String,
})

</script>

<template>
    <p v-if="props.error" class="text-danger mt1">
        {{ props.error }}
    </p>
</template>