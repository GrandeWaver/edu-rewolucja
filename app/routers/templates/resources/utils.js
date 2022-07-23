function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function createUserCookie(email){
  var expire_date = new Date(new Date().getTime()+60*60*1000*8765).toGMTString(); // 1 year
  document.cookie = "userCookie="+email+"; expires="+expire_date+"; path=/";
}

function deleteCookie(name) {
    if( getCookie(name)){
      document.cookie = name + "= o_O ;expires=Thu, 01 Jan 1970 00:00:01 GMT";
    }
  }

function resetVal(val){
  val.notValidCEmail1 = false
  val.notValidCEmail2 = false
  val.notValidPassword = false


  val.notValidREmail = false
  val.emptyFieldFirstname = false
  val.emptyFieldLastname = false
  val.emailExists = false
  val.passwordTooShort = false
}

function resetScreens(sc){
  sc.showSignUp = false
  sc.showSignIn = false
  sc.showWelcomeBack = false
  sc.showSignUpTutor = false
  sc.showPanel = false
  sc.showContact = false
  sc.showPrivacyPolicy = false
  sc.showTermsAndConditions = false
  sc.showClass = false
  sc.showPost = false
  sc.showNewclass1 = false
  sc.showNewclass2 = false
  sc.showNewclass3 = false
}

function handleCredentialResponse(response) {
  $.ajax({
    url: "/auth/googleuser",
    method: 'POST',
    data: JSON.stringify({ 
      token: response.credential,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    success: function(a, b, c){
      var access_token = JSON.parse(c.responseText)
      access_token = access_token["access_token"]

      var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
      document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
      window.location.href = '/'
        },
    error: function(e){
      alert(e.responseJSON.detail)
    }
    },)
 }

 function splitUrl(url){
    new_url = url
    if(new_url.includes("#")){
      new_url = new_url.split('#')[0]
    }
    return new_url
 }

async function getData(url = ''){
  const response = await fetch(url, {
    dataType: "json",
    headers: headersAuth,
  })
    return response.json()
}

 async function getSchedules(_this, classes){
  list_id = []
  classes.map(value => {list_id.push(value.id)})

  let i = 0;
  for (const e of list_id){
    await getData(url+"classes/schedules/"+_this.classes[i].id)
      .then(data => {
        _this.schedules.push(data)
        i++
      })
  }
 }

 function pushToschedule(_this, selected_day){
  let last_index = Object.keys(_this.availability[selected_day][0].schedule).length
  if(last_index == 0){
    _this.availability[selected_day][0].schedule.push(
      {
        start: 11,
        end: 16
      }
    )
    return
  }
  last_hour_start = parseInt(_this.availability[selected_day][0].schedule[last_index-1].start)
  last_hour_end = parseInt(_this.availability[selected_day][0].schedule[last_index-1].end)
  // walidacja 24 godzin
  if(last_hour_end >= 24){
    return
  }
  else{
    if(last_hour_end + 3 > 24){
      last_hour_end = 24
      _this.availability[selected_day][0].schedule.push(
        {
          start: last_hour_end - 1,
          end: last_hour_end
        }
      )
    }
    else{
      _this.availability[selected_day][0].schedule.push(
        {
          start: last_hour_end + 1,
          end: last_hour_end + 3
        }
      )
    }
  }
 }

 function importAvailability(_this){
  _this.availability = 
  {
    "Pn":[
       {
          "name":"poniedziałek",
          "available":true,
          "schedule":[
             {
                "start":11,
                "end":16
             }
          ]
       }
    ],
    "Wt":[
       {
          "name":"wtorek",
          "available":true,
          "schedule":[
             {
                "start":11,
                "end":16
             }
          ]
       }
    ],
    "Śr":[
       {
          "name":"środa",
          "available":true,
          "schedule":[
             {
                "start":11,
                "end":16
             }
          ]
       }
    ],
    "Cz":[
       {
          "name":"czwartek",
          "available":true,
          "schedule":[
             {
                "start":11,
                "end":16
             }
          ]
       }
    ],
    "Pt":[
       {
          "name":"piątek",
          "available":true,
          "schedule":[
             {
                "start":11,
                "end":16
             }
          ]
       }
    ],
    "Sb":[
       {
          "name":"sobota",
          "available":true,
          "schedule":[
             {
                "start":8,
                "end":16
             }
          ]
       }
    ],
    "Nd":[
       {
          "name":"niedziela",
          "available":false,
          "schedule":[
             
          ]
       }
    ]
 }
 }

 function codeRank(rank_encoded){
  let rank_coded = ''

  if(rank_encoded.includes("początkujący")){
    rank_coded += '1'
  }
  if(rank_encoded.includes("podstawowy")){
    rank_coded += '2'
  }
  if(rank_encoded.includes("średni")){
    rank_coded += '3'
  }
  if(rank_encoded.includes("zaawansowany")){
    rank_coded += '4'
  }
  
  return rank_coded
 }