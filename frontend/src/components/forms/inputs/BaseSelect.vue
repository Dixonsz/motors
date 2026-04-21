<script setup>
/**
 * Opcion renderizable dentro de BaseSelect.
 *
 * Attributes:
 *   label (string): Texto visible de la opcion.
 *   value (string|number|boolean): Valor emitido al seleccionar.
 */

/**
 * Propiedades admitidas por BaseSelect.
 *
 * Attributes:
 *   modelValue (string|number|boolean, optional): Valor seleccionado actual.
 *   options (Array): Lista de opciones del selector.
 */
const props = defineProps({
    modelValue: [String, Number, Boolean],
    options: {
        type: Array,
        required: true,
        default: () => [],
    },
})

const emit = defineEmits(['update:modelValue'])

/**
 * Emite el valor elegido en el selector.
 *
 * Args:
 *   event (Event): Evento change del select.
 *
 * Returns:
 *   void
 */
const handleChange = (event) => {
    const target = /** @type {HTMLSelectElement | null} */ (event.target)
    emit('update:modelValue', target?.value ?? '')
}

</script>

<template>
    <select :value="props.modelValue" @change="handleChange">
        <option v-for="option in props.options"
         :key="option.value"
          :value="option.value">
            {{ option.label }}
        </option>
    </select>
</template>
