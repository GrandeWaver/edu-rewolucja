let app = Vue.createApp({ 
    el: "#app",

    data: function(){
      return { 
          showLoading: true,
          showSignUp: false,
          showSignIn: false,
          showWelcomeBack: false,
          showSignInWrong: false,
          showSignUpTutor: false,
          showPanel: false,
          showContact: false,
          showPrivacyPolicy: false,
          userData: [],
          posts: [],
          notValidPassword: false,
          notValidCEmail1: false,
          notValidCEmail2: false,
          emailExists: false,
          emptyFieldFirstname: false,
          emptyFieldLastname: false,
          notValidREmail: false,
          passwordTooShort: false,
          isUserAuthenticated: false,
      };
    },

    mounted : function() {
      this.init()
    },

    methods : {
       href: function(url){
          window.location.href = '/#'+url
          this.showScreen(url)
       },
       showScreen: function(screen) {
          var url = window.location.href
          var hash = url.split('#')[1]
          if (hash) {
            $(".loading").css("display", "none")
            screen = 'show'+hash
          } 

          const _this = this
          console.log(screen + ' opening')

          _this.showLoading = true
          
          if(screen == 'showSignUp'){
              window.location.href = '/#SignUp'
              _this.showLoading = false
              _this.showSignUp = true
              _this.showSignIn = false
              _this.showWelcomeBack = false
              _this.showSignUpTutor = false
              _this.showPanel = false
              _this.showContact = false
              _this.showPrivacyPolicy = false
              console.log('pętla zwrotna rejestracji')
          }
          else if(screen == 'showSignIn'){
            window.location.href = '/#SignIn'
              _this.showLoading = false
              _this.showSignUp = false
              _this.showSignIn = true
              _this.showWelcomeBack = false
              _this.showSignUpTutor = false
              _this.showPanel = false
              _this.showContact = false
              _this.showPrivacyPolicy = false
              console.log('pętla zwrotna logowania')
          }
          else if(screen == 'showWelcomeBack'){
            window.location.href = '/#WelcomeBack'
            _this.showLoading = false
            _this.showSignUp = false
            _this.showSignIn = false
            _this.showWelcomeBack = true
            _this.showSignUpTutor = false
            _this.showPanel = false
            _this.showContact = false
            _this.showPrivacyPolicy = false
        }
          else if(screen == 'showSignUpTutor'){
              window.location.href = '/#SignUpTutor'
              _this.showLoading = false
              _this.showSignUp = false
              _this.showSignIn = false
              _this.showWelcomeBack = false
              _this.showSignUpTutor = true
              _this.showPanel = false
              _this.showContact = false
              _this.showPrivacyPolicy = false
          }
          else if(screen == 'showPanel'){
              window.location.href = '/#Panel'
              _this.showLoading = false
              _this.showSignUp = false
              _this.showSignIn = false
              _this.showWelcomeBack = false
              _this.showSignUpTutor = false
              _this.showPanel = true
              _this.showContact = false
              _this.showPrivacyPolicy = false
              _this.loadPosts()
          }
          else if(screen == 'showContact'){
              window.location.href = '/#Contact'
              _this.showLoading = false
              _this.showSignUp = false
              _this.showSignIn = false
              _this.showWelcomeBack = false
              _this.showSignUpTutor = false
              _this.showPanel = false
              _this.showContact = true
              _this.showPrivacyPolicy = false
          }
          else if(screen == 'showPrivacyPolicy'){
              window.location.href = '/#PrivacyPolicy'
              _this.showLoading = false
              _this.showSignUp = false
              _this.showSignIn = false
              _this.showWelcomeBack = false
              _this.showSignUpTutor = false
              _this.showPanel = false
              _this.showContact = false
              _this.showPrivacyPolicy = true
          }
      },
      init: function(){
        var url = window.location.href
        var hash = url.split('#')[1]
        const _this = this
          $.ajax({
              url: "/auth/",
              method: 'GET',
              headers: {
                  "Content-Type": "application/json",
                  "Authorization": "Bearer "+getCookie('auth')
              },
              success: function(userData){
                  _this.isUserAuthenticated = true
                  _this.userData = userData
                  console.log(_this.userData)
                  console.log(hash)
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
                  else {
                    _this.href('SignIn')
                  }
              }
              },)
      },
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
                  _this.notValidPassword = false
                  var access_token = JSON.parse(c.responseText)
                  access_token = access_token["access_token"]

                  var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
                  document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
                  _this.init()
                  },
              error: function(e){
                console.log(e.responseJSON.detail)
                _this.notValidPassword = true
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
                  _this.href('SignIn')
                  },
              error: function(e){
                if(e.responseJSON.detail[0].msg == 'value is not a valid email address'){
                    //alert('nieprawidłowy adres email')
                    _this.notValidREmail = true
                    _this.emptyFieldFirstname = false
                    _this.emptyFieldLastname = false
                    _this.emailExists = false
                    _this.passwordTooShort = false
                }
                else if(e.responseJSON.detail == 'Empty field: firstname'){
                    // alert('puste pole: imie')
                    _this.notValidREmail = false
                    _this.emptyFieldFirstname = true
                    _this.emptyFieldLastname = false
                    _this.emailExists = false
                    _this.passwordTooShort = false
                }
                else if(e.responseJSON.detail == 'Empty field: lastname'){
                    // alert('puste pole: nazwisko')
                    _this.notValidREmail = false
                    _this.emptyFieldFirstname = false
                    _this.emptyFieldLastname = true
                    _this.emailExists = false
                    _this.passwordTooShort = false
                }
                else if(e.responseJSON.detail == 'User already exists'){
                    // alert('Użytkownik z tym adresem e-mail już istnieje.')
                    _this.notValidREmail = false
                    _this.emptyFieldFirstname = false
                    _this.emptyFieldLastname = false
                    _this.emailExists = true
                    _this.passwordTooShort = false
                }
                else if(e.responseJSON.detail == 'Password is too short'){
                    // alert('hasło jest za krótkie (min 6 znaków)')
                    _this.notValidREmail = false
                    _this.emptyFieldFirstname = false
                    _this.emptyFieldLastname = false
                    _this.emailExists = false
                    _this.passwordTooShort = true
                }
                console.log(e.responseJSON)
              }
              },)
      },
      loadPosts: function () {
        url = document.URL
        if(url.includes("#")){
            url = url.split('#')[0]
        }
        const _this = this
        $.ajax({
          method: "GET",
          url: url+"posts/",
          dataType: "json",
          headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer "+getCookie('auth')
          },
          success: function (posts){
              console.log(posts)
              _this.posts = posts;
         }});
      },
      logout: function(){
          const _this = this
          document.cookie = "auth=let's clean up; expires=Sat, 20 Jan 1980 12:00:00 UTC; path=/";
          _this.init()
      },
      checkEmailFunc: function(){
        const _this = this
        _this.userData.email = $('#Cemail').val()
        console.log(_this.userData)
        $.ajax({
            url: "/users/check",
            method: 'POST',
            data: JSON.stringify({ 
                email: $('#Cemail').val(),
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            success: function(a,b,c){
                if(a.response == 'true'){
                    _this.href('WelcomeBack')
                }
                else{
                    _this.notValidCEmail1 = true
                    _this.notValidCEmail2 = false
                }
                },
            error: function(e){
                _this.notValidCEmail2 = true
                _this.notValidCEmail1 = false
            }
            },)
      }
    }
  })
  app.mount('#app')