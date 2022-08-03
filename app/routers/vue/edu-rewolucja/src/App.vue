<template>
  <Header 
    :loading="loading" 
    :isAuthenticated="isAuthenticated" 
    :userData="userData"
  />
  <br><br>
  <router-view />
  <Footer />
</template>

<script>
import Header from './components/Header-Item.vue'
import Footer from './components/Footer-Item.vue'
import auth from './scripts/utils'

export default {
  name: 'App',
  components: {
    Header, Footer
  },
  data() {
    return {
        loading: true,
        isAuthenticated: undefined,
        userData: [
          {'id': undefined, 'account_type': undefined}
        ]
      }
  },
  mounted : async function() {
    await auth.isAuthenticatedFunc(this)
    // if ciasteczko jest podrobione => usuń je i odswież stronę lub przenies na login
    if(!this.isAuthenticated){
      this.$router.push({ name: 'Login', query: { redirect: '/login' } })
    }
    console.log(this.userData)
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
</style>
