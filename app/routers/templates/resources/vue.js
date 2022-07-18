const headersAuth = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "+getCookie('auth')
}

const app = new Vue({ 
    el: "#app",
    data: {
      showLoading: true,
      sc: [], //screens
      userData: [],
      classes: [],
      schedules: [],
      posts: [],
      isUserAuthenticated: false,
      currClass: [],
      currSchedules: []
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
          }
          else if(screen == 'showSignIn'){
            window.location.href = '/signin'
              resetScreens(_this.sc)
              _this.sc.showSignIn = true
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
            _this.currClass = [] //czyszczenie pamięci
            _this.posts = [] //czyszczenie pamięci
            _this.currSchedules = [] //czyszczenie pamięci
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
// ---------------------------- utils --------------------------------------
      logout: function(){
          deleteCookie('auth')
          deleteCookie('userCookie')
          window.location.href = '/signin'
      },
// ---------------------------- load application data --------------------------------------
      loadPosts: function (class_id) {
        const _this = this
        url = splitUrl(document.URL)
        getData(url+"posts/classes/"+class_id)
        .then(data => {
          _this.currClass = data
          getData(url+"posts/"+class_id)
            .then(data => {
              _this.posts = data
              getData(url+"posts/schedules/"+class_id)
                .then(data => {
                  _this.currSchedules = data
            })
          })
        })
      },
      loadClasses: function () {
        const _this = this
        url = splitUrl(document.URL)
        getData(url+"posts/classes/")
          .then(data => {
            _this.classes = data
            getSchedules(_this, data)
            console.log(_this.classes)
          })


        // $.ajax({
        //   method: "GET",
        //   url: url+"posts/classes/",
        //   dataType: "json",
        //   headers: headersAuth,
        //   success: function (classes){
        //       _this.classes = classes;
        //       for (let i in classes){
        //         setTimeout(() => {
        //           $.ajax({
        //             method: "GET",
        //             url: url+"posts/schedules/"+classes[i].id,
        //             dataType: "json",
        //             headers: headersAuth,
        //             success: function (schedules){
        //               console.log(schedules)
        //                 // _this.classes.push(schedules);
        //                 // console.log(classes)
        //           }});
        //        }, 50) // NAPRAW TO !!!!!!!  SZYBKO !!
        //       }
        //   }});
      },
    }
  })