import { createApp } from 'vue';
import App from './App.vue'
import router from './router'
import "./assets/css/global.css"
import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App)

app.use(
  router
)

app.use(vue3GoogleLogin, {
  clientId: '365589210157-88s142dtgt2e1hd4muaiqbj6bb96dm5b.apps.googleusercontent.com'
})

app.mount('#app')

