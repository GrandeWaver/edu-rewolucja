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
          // tu wysyłany jest tylko token, który backend sam sobie odszyfruje
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