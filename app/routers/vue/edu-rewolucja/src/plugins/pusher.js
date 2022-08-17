export default (app, { apiKey, ...options }) => {
    const Pusher = require('pusher-js')
    app.config.globalProperties.$pusher = new Pusher(apiKey, options)
  }