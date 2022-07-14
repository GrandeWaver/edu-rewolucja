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

// function isUserCookie(){
//     console.log("wywołanie funckjji: isUserCookie()")
//     let cookie = getCookie('userCookie')
//     if (cookie == undefined){
//         createUserCookie()
//         var isCookie = false
//     }
//     else {
//         var isCookie = true
//     }
//     return isCookie
// }

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
}

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

function handleCredentialResponse(response) {
    // decode the credential response from google.
    const responsePayload = parseJwt(response.credential);

   $.ajax({
         url: "/auth/googleuser",
         method: 'POST',
         data: JSON.stringify({ 
           iss: responsePayload.iss,
           firstname: responsePayload.given_name,
           lastname: responsePayload.family_name,
           picture: responsePayload.picture,
           email: responsePayload.email,
           email_verified: responsePayload.email_verified,
           sub: responsePayload.sub
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