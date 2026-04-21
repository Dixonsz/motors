<script setup>
/**
 * Propiedades admitidas por BaseCheckbox.
 *
 * Attributes:
 *   modelValue (boolean, optional): Estado actual del checkbox.
 *   label (string, optional): Texto visible junto al control.
 *   disabled (boolean, optional): Indica si el campo esta deshabilitado.
 */
const props = defineProps({
    modelValue: Boolean,
    label: String,
    disabled: Boolean,
})

const emit = defineEmits(['update:modelValue'])

/**
 * Propaga el cambio de estado del checkbox al componente padre.
 *
 * Args:
 *   event (Event): Evento change del input.
 *
 * Returns:
 *   void
 */
const onChange = (event) => {
        const target = /** @type {HTMLInputElement | null} */ (event.target)
        emit('update:modelValue', target?.checked ?? false)
}

</script>

<template>
    <label class="base-checkbox">
        <input
            type="checkbox"
            class="base-checkbox-input"
            :checked="props.modelValue"
            :disabled="props.disabled"
            @change="onChange"
        />
        <span class="base-checkbox-label">
            {{ props.label }}
        </span>
    </label>
</template>