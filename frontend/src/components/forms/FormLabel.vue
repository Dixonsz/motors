<script setup>
/**
 * Propiedades admitidas por FormLabel.
 *
 * Attributes:
 *   label (string, optional): Texto de la etiqueta.
 *   forId (string, optional): Id del campo asociado.
 *   required (boolean, optional): Indica si el campo es obligatorio.
 */
const props = defineProps({
    label: String,
    forId: String,
    required: Boolean,
})

</script>

<template>
    <label v-if="props.label" :for="props.forId" class="form-label">
        {{ props.label }}
        <span v-if="props.required" class="text-danger">*</span>
    </label>
</template>