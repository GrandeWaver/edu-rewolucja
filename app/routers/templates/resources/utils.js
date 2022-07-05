function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    }

// function createUserCookie(){
//     var expire_date = new Date(new Date().getTime()+60*60*1000*8765).toGMTString(); // 1 year
//     document.cookie = "userCookie=<3; expires="+expire_date+"; path=/";
// }

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


