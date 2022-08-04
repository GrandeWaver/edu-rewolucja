import cookies from "./cookies"
import getData from "./getData"

var auth = {
    async isAuthenticatedFunc(_this){
        var userData = []
        var url = getData.url()
        if (cookies.getCookie('auth') == undefined){
          _this.isAuthenticated = false
          _this.$router.push({ name: 'Login' })
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

          // $.ajax({
          //     url: "/auth/",
          //     method: 'GET',
          //     headers: headersAuth,
          //     success: function(userData){
          //         // przekierowania
          //         if (hash == 'WelcomeBack') {
          //           _this.href('Panel')
          //         }
          //         else if (hash) { // dostęp do wszystkiego
          //           _this.href(hash)
          //         }
          //         else {
          //           _this.href('Panel')
          //         }
          //         return userData
          //         },
          //     error: function(e){
          //       _this.isUserAuthenticated = false
          //       if (hash == 'SignUp') {
          //           _this.href('SignUp')
          //         }
          //         else if (hash == 'SignUpTutor') {
          //           _this.href('SignUpTutor')
          //         }
          //         else if (hash == 'Contact') {
          //           _this.href('Contact')
          //         }
          //         else if (hash == 'PrivacyPolicy') {
          //           _this.href('PrivacyPolicy')
          //         }
          //         else if (hash == 'TermsAndConditions') {
          //           _this.href('TermsAndConditions')
          //         }
          //         else {
          //           if(_this.userData.email){
          //             _this.href('WelcomeBack')
          //           }
          //           else {
          //             window.location.href = '/signin'
          //           }
          //         }
          //     }
          //     },)
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