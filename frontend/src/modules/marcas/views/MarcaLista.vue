<script setup>
import { onMounted, ref } from 'vue'
import { getMarcas } from '../services/marcaService'

const marcas = ref([])
const loading = ref(false)
const error = ref('')

const cargarMarcas = async () => {
	loading.value = true
	error.value = ''

	try {
		const response = await getMarcas()
		marcas.value = Array.isArray(response) ? response : []
	} catch (err) {
		error.value = 'No se pudo cargar la lista de marcas. Verifica sesion y API.'
		marcas.value = []
	} finally {
		loading.value = false
	}
}

onMounted(cargarMarcas)
</script>

<template>
	<section class="marca-lista">
		<header class="header">
			<h1>Marcas</h1>
			<button type="button" class="btn-recargar" @click="cargarMarcas" :disabled="loading">
				{{ loading ? 'Cargando...' : 'Recargar' }}
			</button>
		</header>

		<p v-if="loading" class="estado">Cargando marcas...</p>
		<p v-else-if="error" class="error">{{ error }}</p>
		<p v-else-if="marcas.length === 0" class="estado">No hay marcas registradas.</p>

		<table v-else class="tabla-marcas">
			<thead>
				<tr>
					<th>ID</th>
					<th>Nombre</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="marca in marcas" :key="marca.id">
					<td>{{ marca.id }}</td>
					<td>{{ marca.nombre }}</td>
				</tr>
			</tbody>
		</table>
	</section>
</template>

<style scoped>
.marca-lista {
	display: grid;
	gap: 1rem;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.btn-recargar {
	padding: 0.5rem 0.9rem;
	border: 1px solid #cfd4dc;
	border-radius: 0.5rem;
	background: #fff;
	cursor: pointer;
}

.btn-recargar:disabled {
	opacity: 0.7;
	cursor: not-allowed;
}

.estado {
	color: #4b5563;
}

.error {
	color: #c1121f;
}

.tabla-marcas {
	width: 100%;
	border-collapse: collapse;
	background: #fff;
}

.tabla-marcas th,
.tabla-marcas td {
	border: 1px solid #e5e7eb;
	padding: 0.6rem;
	text-align: left;
}

.tabla-marcas thead {
	background: #f3f4f6;
}
</style>



