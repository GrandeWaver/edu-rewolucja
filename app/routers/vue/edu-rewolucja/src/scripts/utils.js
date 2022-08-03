import cookies from "./cookies"
import getData from "./getData"

var auth = {
    async isAuthenticatedFunc(_this){
        var url = getData.url()
        if (cookies.getCookie('auth') == undefined){
          _this.isAuthenticated = false
          _this.loading = false
          _this.$router.push({ name: 'Login', query: { redirect: '/login' } })
        } else {
          await getData.getData(_this, url+"/auth/")
          .then(data => {
            _this.isAuthenticated = true
            _this.userData = data
          })
          .catch(() => {
            cookies.deleteCookie('auth')
            _this.isAuthenticated = false
            _this.loading = false
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
    },
    logoutFunc(){
        cookies.deleteCookie('auth')
    }
}

export default auth