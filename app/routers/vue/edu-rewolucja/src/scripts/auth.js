import cookies from "./cookies"
import getData from "./getData"

var auth = {
    async isAuthenticatedFunc(_this){
        var userData = []
        var url = getData.url()
        if (cookies.getCookie('auth') == undefined){
          _this.isAuthenticated = false
        } else {
          await getData.getData(_this, url+"/auth/")
          .then(data => {
            _this.isAuthenticated = true
            userData = data
          })
          .catch(() => {
            cookies.deleteCookie('auth')
            _this.isAuthenticated = false
            _this.$router.push({ name: 'Login', query: { redirect: '/login' } })
          })
        }
        if(userData.length != 0){
          if(!String(userData.picture).startsWith('https://')){
            userData.picture = getData.url()+userData.picture
          }
        }
        return userData
    },
    createLoginCookie(responseJSON){
      let access_token = responseJSON.access_token
      var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
      document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
      window.location.replace("/")
    },
    logoutFunc(){
        cookies.deleteCookie('auth')
    }
}

export default auth