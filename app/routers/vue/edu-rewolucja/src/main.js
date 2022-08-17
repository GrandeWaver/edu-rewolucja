import { createApp } from 'vue';
import App from './App.vue'
import router from './router'
import "./assets/css/global.css"
import vue3GoogleLogin from 'vue3-google-login'
import { store } from './store/index'
import PusherPlugin from './plugins/pusher'

const app = createApp(App)

app.use(
  router
)

app.use(
  store
)

app.use(
  PusherPlugin, {
    apiKey: '94fb841a5b6a5b0fd651', 
    cluster: 'eu'
  }
)

app.use(vue3GoogleLogin, {
  clientId: '365589210157-88s142dtgt2e1hd4muaiqbj6bb96dm5b.apps.googleusercontent.com'
})

app.mount('#app')

