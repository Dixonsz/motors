<template>
  <main>
    <nav>
      <RouterLink to="/marcas">Ver marcas</RouterLink>
    </nav>
    <RouterView />
  </main>
</template>

<style scoped>
main {
  padding: 1rem;
}

nav {
  margin-bottom: 1rem;
}
</style>