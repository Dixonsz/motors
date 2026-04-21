<script setup>
import {reactive, ref} from 'vue'

import BaseForm from '@/components/forms/BaseForm.vue'
import FormField from '@/components/forms/FormField.vue'
import FormLabel from '@/components/primitives/BaseInput.vue'
import BaseButton from '@/components/primitives/BaseButton.vue'

const formData = reactive({
    nombre: '',
})

const errors = reactive({})
const loading = ref(false)

const save = () => {
    errors.nombre = ''

    if(!formData.nombre){
        errors.nombre = 'El nombre es requerido'
        return  
    }
    Alert('Guardando marca: ' + formData.nombre)
}

<template>
    <BaseForm @submit="save">
    <FormField label="Nombre" :error="errors.nombre" required>
        <BaseInput v-model="formData.nombre" placeholder="Ingrese el nombre de la marca" />
    </FormField>

    <BaseButton type="submit" :disabled="loading">
        {{ loading ? 'Guardando...' : 'Guardar' }}
    </BaseButton>
    </BaseForm>
</template>
       


