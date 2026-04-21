<script setup>

import FormError from './FormError.vue'

/**
 * Propiedades admitidas por FormField.
 *
 * Attributes:
 *   label (string, optional): Etiqueta visual del campo.
 *   error (string, optional): Mensaje de error asociado al campo.
 */
const props = defineProps({
    label: String,
    error: String,
})
</script>

<template>
    <div class="form-field">
        <label v-if="props.label" class="form-label">
            {{ props.label }}
        </label>
        <slot></slot>
        <FormError :error="props.error" />
    </div>
</template>