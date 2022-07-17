const headersAuth = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "+getCookie('auth')
}

const app = new Vue({ 
    el: "#app",
    data: {
      showLoading: true,
      sc: [], //screens
      val: [], // walidacja formularzy
      userData: [],
      classes: [],
      posts: [],
      isUserAuthenticated: false,
      currClass: [],
      // messages: [],
    },
    mounted : function() {
      this.init()
    },

    methods : {
       href: function(url){
          const _this = this
          _this.showLoading = true
          window.location.href = '/#'+url
          _this.showScreen(url)
       },
       showScreen: function(screen) {
          const _this = this
          var url = window.location.href
          var hash = url.split('#')[1]
          if (hash) {
            _this.showLoading = false
            screen = 'show'+hash

            number = url.split('Class')[1] // numer zajęć, które klient chce zobaczyć
            if(number){
              screen = 'showClass' // wyczyszczenie numeru, po to aby wyświetlić screen
            }
          }
          console.log(screen + ' opening')
        
          if(screen == 'showSignUp'){
              window.location.href = '/signup'
              resetScreens(_this.sc)
              _this.sc.showSignUp = true
              resetVal(_this.val)
          }
          else if(screen == 'showSignIn'){
            window.location.href = '/signin'
              resetScreens(_this.sc)
              _this.sc.showSignIn = true
              resetVal(_this.val)
          }
          else if(screen == 'showWelcomeBack'){
            window.location.href = '/welcomeback'
            resetScreens(_this.sc)
            _this.sc.showWelcomeBack = true
        }
          else if(screen == 'showSignUpTutor'){
              window.location.href = '/#SignUpTutor'
              resetScreens(_this.sc)
              _this.sc.showSignUpTutor = true
          }
          else if(screen == 'showContact'){
              window.location.href = '/#Contact'
              resetScreens(_this.sc)
              _this.sc.showContact = true
          }
          else if(screen == 'showPrivacyPolicy'){
              window.location.href = '/#PrivacyPolicy'
              resetScreens(_this.sc)
              _this.sc.showPrivacyPolicy = true
          }
          else if(screen == 'showTermsAndConditions'){
            window.location.href = '/#TermsAndConditions'
            resetScreens(_this.sc)
            _this.sc.showTermsAndConditions = true
          }
          else if(screen == 'showPanel'){
            window.location.href = '/#Panel'
            resetScreens(_this.sc)
            _this.sc.showPanel = true
            _this.loadClasses()
        }
        else if(screen == 'showClass'){
          window.location.href = '/#Class'+number
          resetScreens(_this.sc)
          _this.sc.showClass = true
          _this.loadPosts(number)
        }
      },
      init: function(){
        const _this = this
        var hash = window.location.href.split('#')[1]
        var userEmailCookie = getCookie("userCookie")
        _this.userData.email = userEmailCookie
          $.ajax({
              url: "/auth/",
              method: 'GET',
              headers: headersAuth,
              success: function(userData){
                  _this.isUserAuthenticated = true
                  _this.userData = userData
                  console.log(_this.userData)
                  // przekierowania
                  if (hash == 'WelcomeBack') {
                    _this.href('Panel')
                  }
                  else if (hash) { // dostęp do wszystkiego
                    _this.href(hash)
                  }
                  else {
                    _this.href('Panel')
                  }
                  },
              error: function(e){
                _this.isUserAuthenticated = false
                if (hash == 'SignUp') {
                    _this.href('SignUp')
                  }
                  else if (hash == 'SignUpTutor') {
                    _this.href('SignUpTutor')
                  }
                  else if (hash == 'Contact') {
                    _this.href('Contact')
                  }
                  else if (hash == 'PrivacyPolicy') {
                    _this.href('PrivacyPolicy')
                  }
                  else if (hash == 'TermsAndConditions') {
                    _this.href('TermsAndConditions')
                  }
                  else {
                    if(_this.userData.email){
                      _this.href('WelcomeBack')
                    }
                    else {
                      window.location.href = '/signin'
                    }
                  }
              }
              },)
      },
      // --------------------------------- formularze ---------------------------------
      signInFunc: function(){
          const _this = this
          $.ajax({
              url: "/auth/",
              method: 'POST',
              data: { 
                  username: _this.userData.email,
                  password: $('#Lpassword').val()
                  },
              contentType: 'application/x-www-form-urlencoded',
              success: function(a,b,c){
                  _this.val.notValidPassword = false
                  var access_token = JSON.parse(c.responseText)
                  access_token = access_token["access_token"]

                  var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
                  document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
                  _this.init()
                  },
              error: function(e){
                console.log(e.responseJSON.detail)
                _this.val.notValidPassword = true
              }
              },)
      },
      signUpFunc: function(){
          const _this = this
          _this.userData.email = $('#Remail').val()
          _this.userData.firstname = $('#Rfirstname').val()
          _this.userData.lastname = $('#Rlastname').val()
          $.ajax({
              url: "/users/",
              method: 'POST',
              data: JSON.stringify({ 
                  email: _this.userData.email,
                  firstname: _this.userData.firstname,
                  lastname: _this.userData.lastname,
                  password: $('#Rpassword').val()
                  }),
              contentType: 'application/json',
              success: function(){
                  _this.val.notValidCEmail1 = false
                  window.location.href = '/signin'
                  },
              error: function(e){
                if(e.responseJSON.detail[0].msg == 'value is not a valid email address'){
                  resetVal(_this.val)
                  _this.val.notValidREmail = true
                }
                else if(e.responseJSON.detail == 'Empty field: firstname'){
                  resetVal(_this.val)
                  _this.val.emptyFieldFirstname = true
                }
                else if(e.responseJSON.detail == 'Empty field: lastname'){
                  resetVal(_this.val)
                  _this.val.emptyFieldLastname = true
                }
                else if(e.responseJSON.detail == 'User already exists'){
                  resetVal(_this.val)
                  _this.val.emailExists = true
                }
                else if(e.responseJSON.detail == 'Password is too short'){
                  resetVal(_this.val)
                  _this.val.passwordTooShort = true
                }
                console.log(e.responseJSON)
              }
              },)
      },
      logout: function(){
          deleteCookie('auth')
          deleteCookie('userCookie')
          window.location.href = '/signin'
      },
      checkEmailFunc: function(){
        const _this = this
        _this.userData.email = $('#Cemail').val()
        console.log(_this.userData)
        createUserCookie(_this.userData.email)
        $.ajax({
            url: "/users/check",
            method: 'POST',
            data: JSON.stringify({ 
                email: $('#Cemail').val(),
                }),
                headers: {"Content-Type": "application/json"},
            success: function(a,b,c){
                if(a.response == 'true'){
                    _this.href('WelcomeBack')
                }
                else{
                    _this.val.notValidCEmail1 = true
                    _this.val.notValidCEmail2 = false
                }
                },
            error: function(e){
                _this.val.notValidCEmail2 = true
                _this.val.notValidCEmail1 = false
            }
            },)
      },
// ---------------------------- load application data --------------------------------------
      loadPosts: function (class_id) {
        const _this = this
        url = splitUrl(document.URL)
        // GET subject AND schedules
        $.ajax({
          method: "GET",
          url: url+"posts/classes/"+class_id,
          dataType: "json",
          headers: headersAuth,
          success: function (currClass){
              _this.currClass = currClass;
              console.log(_this.currClass)
         }});
         setTimeout(() => {
            $.ajax({
            method: "GET",
            url: url+"posts/"+class_id,
            dataType: "json",
            headers: headersAuth,
            success: function (posts){
                _this.posts = posts;
          }});
         }, 30)
      },
      loadClasses: function () {
        const _this = this
        url = splitUrl(document.URL)
        $.ajax({
          method: "GET",
          url: url+"posts/classes/",
          dataType: "json",
          headers: headersAuth,
          success: function (classes){
              _this.classes = classes;
          }});
      },
    }
  })