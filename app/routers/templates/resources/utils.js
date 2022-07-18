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
    await getData(url+"posts/schedules/"+_this.classes[i].id)
      .then(data => {
        _this.schedules.push(data)
        i++
      })
  }

  console.log(_this.classes)
  console.log(_this.schedules)

  // for (let i in classes){
  //   fetch(url+"posts/schedules/"+classes[i].id, {
  //     dataType: "json",
  //     headers: headersAuth,
  //   })
  //     .then(response => response.json())
  //     .then(data => console.log(data))
  // }
 }
