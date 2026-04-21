<script setup>
/**
 * Propiedades admitidas por el componente BaseTextArea.
 *
 * Attributes:
 *   modelValue (string, optional): Valor actual del textarea.
 *   placeholder (string, optional): Texto de ayuda cuando esta vacio.
 */
const props = defineProps({
    modelValue: String,
    placeholder: String,
})

const emit = defineEmits(['update:modelValue'])

/**
 * Maneja el evento de entrada y emite el nuevo valor al componente padre.
 *
 * Args:
 *   event (Event): Evento nativo disparado por el textarea.
 *
 * Returns:
 *   void
 */
function handleInput(event) {
    const target = /** @type {HTMLTextAreaElement | null} */ (event.target)
    emit('update:modelValue', target?.value ?? '')
}
</script>

<template>
    <textarea
        :value="props.modelValue"
        :placeholder="props.placeholder"
        @input="handleInput"
        class="base-textarea"
    ></textarea>
</template>