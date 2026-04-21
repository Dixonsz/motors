<script setup>
/**
 * Propiedades admitidas por BaseRadio.
 *
 * Attributes:
 *   modelValue (string|number|boolean, optional): Valor seleccionado actual.
 *   value (string|number|boolean, optional): Valor asociado a esta opcion.
 *   label (string, optional): Texto visible de la opcion.
 *   name (string, optional): Nombre del grupo de radios.
 *   disabled (boolean, optional): Indica si el control esta deshabilitado.
 */
const props = defineProps({
    modelValue: [String, Number, Boolean],
    value: [String, Number, Boolean],
    label: String,
    name: String,
    disabled: Boolean,
})

const emit = defineEmits(['update:modelValue'])

/**
 * Emite el valor de la opcion cuando es seleccionada.
 *
 * Args:
 *   _event (Event): Evento change del radio.
 *
 * Returns:
 *   void
 */
const onChange = (event) => {
    emit('update:modelValue', props.value)
}

</script>

<template>
    <label class="base-radio">
        <input
            type="radio"
            class="base-radio-input"
            :name="props.name"
            :value="props.value"
            :checked="props.modelValue === props.value"
            :disabled="props.disabled"
            @change="onChange"
        />
        <span class="base-radio-label">
            {{ props.label }}
        </span>
    </label>
</template>