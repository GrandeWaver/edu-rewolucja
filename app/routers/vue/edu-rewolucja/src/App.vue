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
    <div v-if="videocall">
        <VideoCall :data=videocall_data />
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
import VideoCall from './components/VideoCall-Item.vue'

import getData from './scripts/getData'

export default {
  name: 'App',
  components: {
    NprogressContainer, Header, Footer, Alert, VideoCall
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
        alerts: [],
        videocall: false,
        videocall_data: []
      }
  },
  mounted: async function() {
    const _this = this
    _this.userData = await auth.isAuthenticatedFunc(_this)


    // listen to pusher
    
    var alerts = await _this.$pusher.subscribe('alerts')
    await alerts.bind('main', function(data) {
      console.log(data)
      _this.alerts.push(data)
    })
    await alerts.bind(_this.userData.id, function(data) {
      console.log(data)
      _this.alerts.push(data)
    })

    var videocall = await _this.$pusher.subscribe('videocall');
    await videocall.bind(_this.userData.id, function(data) {
      console.log(data)
      if(data.notification.notification == 'start'){
        _this.videocall = true
        _this.videocall_data = data
      }
      // zakończ viedeocall jakoś
    })


    if(_this.isAuthenticated){
      // fetch get check notifications
      fetch(getData.url()+'/notifications/', {headers: getData.getHeaders()})
            .then(r => {
                if(r.status != 200){
                    alert('Error: cannot check notifications')
                    return r
                } else { return r.json() }
            })
            .then(r => {
              if(r.notification.notification == 'start'){
                _this.videocall = true
                _this.videocall_data = r
              }
              console.log(r)
            })
    }
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
