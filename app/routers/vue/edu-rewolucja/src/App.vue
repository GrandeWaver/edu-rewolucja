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
// import cookies from './scripts/cookies'
// import getData from './scripts/getData'

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
  created: async function() {
    this.userData = await auth.isAuthenticatedFunc(this)
    if(this.isAuthenticated){
      this.alerts.push({"text": "Strona w trakcie budowy. Nie wszystko może działać poprawnie."})
    }


  // pusher
  const _this = this
    var channel = this.$pusher.subscribe('alerts');
    channel.bind('main', function(data) {
      console.log(data)
      _this.alerts.push(data);
    })
    channel.bind(_this.userData.id, function(data) {
      console.log(data)
      _this.alerts.push(data);
    })


    // if(this.isAuthenticated){
    //   this.connection = new WebSocket(`${getData.webSocketUrl()}${this.userData.id}?token=${cookies.getCookie('auth')}`)

    //   // handle websocket
    //   const _this = this
    //   this.connection.onmessage = function(event) {
    //     if(event.data.startsWith("alert: ")){
    //       _this.alerts.push({"text": event.data.replace('alert: ','')})
    //     } else {
    //       return
    //     }
    //   }
    // }
  }
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
