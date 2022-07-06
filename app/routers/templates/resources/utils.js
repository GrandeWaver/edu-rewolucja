function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    }

function createUserCookie(email){
    var expire_date = new Date(new Date().getTime()+60*60*1000*8765).toGMTString(); // 1 year
    document.cookie = "userCookie="+email+"; expires="+expire_date+"; path=/";
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

