<script setup>
/**
 * Propiedades admitidas por BaseInput.
 *
 * Attributes:
 *   modelValue (string|number, optional): Valor actual del input.
 *   type (string, optional): Tipo HTML del input.
 *   placeholder (string, optional): Texto de apoyo cuando esta vacio.
 *   disabled (boolean, optional): Indica si el control esta deshabilitado.
 */
const props = defineProps({
    modelValue: [String, Number],
    type: {
        type: String,
        default: 'text',
    },
    placeholder: String,
    disabled: Boolean,
})

const emit = defineEmits(['update:modelValue'])

/**
 * Emite el valor del input cada vez que cambia.
 *
 * Args:
 *   event (Event): Evento input del campo.
 *
 * Returns:
 *   void
 */
const onInput = (event) => {
    const target = /** @type {HTMLInputElement | null} */ (event.target)
    emit('update:modelValue', target?.value ?? '')
}

</script>
<template>
    <input
        :type="props.type"
        :value="props.modelValue"
        :placeholder="props.placeholder"
        :disabled="props.disabled"
        @input="onInput"
        class="base-input"
    />
</template>
