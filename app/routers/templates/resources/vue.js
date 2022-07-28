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
      currSchedules: [],
      currPost: [],
      expandForm: false,
      newPost: [],
      selected_day: "Pn",
      selected_day_index: 0,
      select: {rank: ["początkujący"]}, // domyślnie zaznaczony stopień nauki
      days: ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"],
      availability: {},
      available_tutors: [],
      available_schedules: [],
      select_first_lesson: {day: undefined, month: undefined, month_index: 0, day_index: 0, hour: undefined},
      // messages: [],
    },
    mounted : function() {
      this.init()
      importAvailability(this)
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

            class_id = url.split('Class')[1] // numer zajęć, które klient chce zobaczyć
            if(class_id){
              screen = 'showClass' // wyczyszczenie numeru, po to aby wyświetlić screen
            }

            post_id = url.split('Post')[1] // numer posta, który klient chce zobaczyć
            if(post_id){
              _this.currPost.post_id = post_id
              screen = 'showPost' // wyczyszczenie numeru, po to aby wyświetlić screen
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
          window.location.href = '/#Class'+class_id
          resetScreens(_this.sc)
          _this.sc.showClass = true
          _this.loadPosts(class_id)
        }
        else if(screen == 'showPost'){
          window.location.href = '/#Post'+post_id
          resetScreens(_this.sc)
          _this.sc.showPost = true
          _this.loadCurrPost(post_id)
        }
        else if(screen == 'showNewclass1'){
          window.location.href = '/#Newclass1'
          resetScreens(_this.sc)
          _this.sc.showNewclass1 = true
        }
        else if(screen == 'showNewclass2'){
          window.location.href = '/#Newclass2'
          resetScreens(_this.sc)
          _this.sc.showNewclass2 = true
          _this.available_tutors = [] // czyszczenie pamięci
          _this.loadTutors()
        }
        else if(screen == 'showNewclass3'){
          window.location.href = '/#Newclass3'
          resetScreens(_this.sc)
          _this.sc.showNewclass3 = true
          _this.loadSchedules()
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
      backArrowFunc: function(){
        const _this = this
        var url = window.location.href
        post = url.split('Post')[1]
        if(post){
          _this.href('Class'+_this.currPost[0].class_id)
        }
        else {
          _this.href('Panel')
        }
      },
      logout: function(){
          deleteCookie('auth')
          deleteCookie('userCookie')
          window.location.href = '/signin'
      },
      expandFormFunc: function(){
        const _this = this
        _this.expandForm = true
      },
      hideForm: function(){
        const _this = this
        _this.expandForm = false
      },
      submitPost: function(class_id){
        const _this = this
        _this.newPost.class_id = class_id
        fetch(url+"posts/", {
          method: "POST",
          dataType: "json",
          body: JSON.stringify({
            title: _this.newPost.title,
            content: _this.newPost.content,
            class_id: _this.newPost.class_id
          }),
          headers: headersAuth,
        })
        .then({
          _this: _this.expandForm = false,
          _this: _this.loadPosts(class_id),
          _this: _this.newPost = []
        })
        .then(result => {
          console.log('Success:', result);
        })
        .catch(error => {
          alert('Error:', error);
        })
      },
      selectDay: function (day, index){
        const _this = this
        _this.selected_day = day
        _this.selected_day_index = index
      },
      downDayFunc: function(){
        const _this = this
        if(_this.selected_day_index == 0){
          return
        }
        new_index = _this.selected_day_index-1
        new_day = _this.days[new_index]
        _this.selectDay(new_day, new_index)
      },
      upDayFunc: function(){
        const _this = this
        if(_this.selected_day_index == 6){
          return
        }
        new_index = _this.selected_day_index+1
        new_day = _this.days[new_index]
        _this.selectDay(new_day, new_index)
      },
      changeClass(index) {
        const _this = this
        if(index == _this.selected_day_index){
          return 'selectedDay yes'
        }
        else {
          return 'SelectedDay'
        }
      },
      addSchedule(selected_day){
        const _this = this
        _this.availability[selected_day][0].available = true
        pushToschedule(_this, selected_day)
      },
      deleteSchedule(selected_day){
        const _this = this
        if(Object.keys(_this.availability[selected_day][0].schedule).length == 1){
          _this.availability[selected_day][0].available = false
        }
        _this.availability[selected_day][0].schedule.pop()
      },
      isDictEmpty(selected_day){
        const _this = this
        if(Object.keys(_this.availability[selected_day][0].schedule).length == 0){
          pushToschedule(_this, selected_day)
        }
        if (_this.availability[selected_day][0].available){
          _this.availability[selected_day][0].schedule = []
        }
      },
      submitClassTutor(){
        const _this = this
        let subject = _this.select.subject
        rank_coded = codeRank(_this.select.rank)

        let tutor_id = _this.userData.id
        fetch(url+"create_class/tutor", {
          method: "POST",
          dataType: "json",
          body: JSON.stringify({
            subject: subject,
            rank: rank_coded,
            tutor_id: tutor_id,
            availability: _this.availability
          }),
          headers: headersAuth,
        })
        .then(response => {
          if(response.status == 500){
            alert('error: błąd połączenia z bazą danych... \nkod błędu: 500')
          }
          if(response.status == 418){
            alert('error: Brak wsparcia dla leniów \nkod błędu: 418')
          }
          if(response.status == 409){
            alert('Te zajęcia do tego przedmiotu są już stworzone, poinformujemy cię gdy znajdzie się chętny uczeń')
          }
          _this.href('Panel')
        })
        .catch(error => {
          alert('Error:', error);
        })
      },
// ---------------------------- load application data --------------------------------------
      loadPosts: function (class_id) {
        const _this = this
        url = splitUrl(document.URL)
        getData(_this, url+"classes/details/"+class_id)
        .then(data => {
          _this.currClass = data
          getData(_this, url+"posts/"+class_id)
            .then(data => {
              _this.posts = data
              getData(_this, url+"classes/schedules/"+class_id)
                .then(data => {
                  _this.currSchedules = data
                  _this.showLoading = false
            })
          })
        })
      },
      loadClasses: function () {
        const _this = this
        _this.schedules = [] // czyszczenie pamięci
        url = splitUrl(document.URL)
        getData(_this, url+"classes/")
          .then(data => {
            _this.classes = data
            getSchedules(_this, data)
          })
      },
      loadCurrPost: function (post_id){
        const _this = this
        _this.schedules = [] // czyszczenie pamięci
        _this.currPost = [] // czyszczenie pamięci
        url = splitUrl(document.URL)
        getData(_this, url+"posts/details/"+post_id)
        .then(data => {
          _this.showLoading = false
          _this.currPost = data
        })
      },
      loadTutors(counter = 0){
        const _this = this
        let subject = _this.select.subject
        if(subject == undefined){ // Vue wolniej zapisuje zmienną niż js, który sprawdza czy jest zdefiniowana
          setTimeout(() => {
            if(counter < 40){
              counter = counter + 1
              _this.loadTutors(counter)
            }
            if(counter == 40){
              addClassesAgainError(_this)
            }
          }, 5)
        }
        else if(_this.userData.account_type == 'student'){ //nie jestem z tego rozwiązania dumny jak coś
          url = splitUrl(document.URL)
          getData(_this, url+"select_class/"+subject)
          .then(data => {
            _this.showLoading = false
            _this.available_tutors = data
            console.log(data)
            _this.available_tutors.forEach(function (value, index) {
              encoded = encodeRank(_this.available_tutors[index].rank)
              _this.available_tutors[index].encoded = encoded
            })
          })
        }
      },
      loadSchedules(counter = 0){
        const _this = this
        available_class_id = _this.select.available_class_id
        if(available_class_id == undefined && _this.userData.account_type == 'student'){ // Vue wolniej zapisuje zmienną niż js, który sprawdza czy jest zdefiniowana
          setTimeout(() => {
            if(counter < 40){
              counter = counter + 1
              _this.loadSchedules(counter)
            }
            if(counter == 40){
              addClassesAgainError(_this)
            }
          }, 5)
        }
        else if(_this.userData.account_type == 'student'){
          console.log(available_class_id)
          getData(_this, url+"select_class/schedules/"+available_class_id)
          .then(data => {
            _this.showLoading = false
            console.log(data)
            _this.available_schedules = data
            _this.select_first_lesson.day = data[_this.select_first_lesson.month_index].days[_this.select_first_lesson.day_index].day
            _this.select_first_lesson.month = data[_this.select_first_lesson.month_index].month
            _this.select_first_lesson.year = data[_this.select_first_lesson.month_index].year
          })
        }
      },
      SignUpForLesson(){
        const _this = this
        var hour_input_value = $("#select_hour").val();
        if(hour_input_value != null){
          fetch(url+"create_class/student", {
            method: "POST",
            dataType: "json",
            body: JSON.stringify({
              month: _this.select_first_lesson.month,
              year: _this.select_first_lesson.year,
              day_name: _this.available_schedules[_this.select_first_lesson.month_index].days[_this.select_first_lesson.day_index].name,
              day: _this.select_first_lesson.day,
              hour: _this.select_first_lesson.hour,
              available_class_id: _this.select.available_class_id
            }),
            headers: headersAuth,
          })
          .then(response => {
            if(response.status == 201){
              _this.href('Panel')
            }
            if(response.status == 500){
              alert('error: błąd połączenia z bazą danych... \nkod błędu: 500')
            }
          })
        console.log('wysyłanie do create_class/student')
        }
      }
    },
  })