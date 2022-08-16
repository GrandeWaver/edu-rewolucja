<template>
  <nprogress-container></nprogress-container>
  <Header 
    :isAuthenticated="isAuthenticated" 
    :userData="userData"
  />
  <div class="page-container">
    <br><br>
    <Alert text="Strona w trakcie budowy. Nie wszystko może działać poprawnie." />
    <Alert text="O godzinie 00:00 odbędzie się lekcja przedmiotu z Imie Nazwisko." />
    <router-view />
  </div>
  <Footer />
</template>

<script>
import Header from './components/Header-Item.vue'
import Footer from './components/Footer-Item.vue'
import auth from './scripts/auth.js'
import NprogressContainer from 'vue-nprogress/src/NprogressContainer'
import Alert from './components/Alert-Item.vue'

export default {
  name: 'App',
  components: {
    NprogressContainer, Header, Footer, Alert
  },
  data() {
    return {
      isAuthenticated: false,
      userData: [
          {
            'id': undefined, 
            'account_type': undefined, 
            'picture': undefined
          }
        ]
      }
  },
  mounted: async function() {
    this.userData = await auth.isAuthenticatedFunc(this)
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nprogress .spinner {
  display: none;
}
.page-container {
    min-height: 98vh;
}
@media only screen and (max-width: 440px) {
.page-container {
    min-height: 94vh;
}
}
</style>
