<template>
  <v-app>
    <v-app-bar fixed app color="primary" dark elevation="0">Proteção Civil</v-app-bar>
    <v-main style="background-color: #88dd88;">
      <v-container class="fill-height d-flex align-center">
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer fixed app color="primary lighten-2" dark>
      <span>nhopf &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data () {
    return {}
  }
}
</script>
