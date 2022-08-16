<template>
  <nprogress-container></nprogress-container>
  <Header 
    :isAuthenticated="isAuthenticated" 
    :userData="userData"
  />
  <div class="page-container">
    <br><br>
    <div v-for="(alert, index) in alerts" :key="index">
        <Alert :text=alert.text />
    </div>
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
import cookies from './scripts/cookies'
import getData from './scripts/getData'

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
        ],
        alerts: []
      }
  },
  mounted: async function() {
    this.userData = await auth.isAuthenticatedFunc(this),
    // this.Alerts.push({"text": "Aplikacja nie działa w twoim kraju. (Problemy ze strefą czasową)"})

    // var channel = this.$pusher.subscribe('my-channel');
    // channel.bind('my-event', function(data) {
    //   this.alerts.push(JSON.stringify(data));
    // });

    this.connection = new WebSocket(`${getData.webSocketUrl()}${this.userData.id}?token=${cookies.getCookie('auth')}`)

    // this.connection.onopen = function(event) {
    // }

    const _this = this
    this.connection.onmessage = function(event) {
      _this.alerts.push({"text": event.data})
    }
    
    this.alerts.push({"text": "Strona w trakcie budowy. Nie wszystko może działać poprawnie."})

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
