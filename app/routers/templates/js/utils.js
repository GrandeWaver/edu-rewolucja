function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    }

function createUserCookie(){
    var expire_date = new Date(new Date().getTime()+60*60*1000*8765).toGMTString(); // 1 year
    document.cookie = "userCookie=<3; expires="+expire_date+"; path=/";
}

function isUserCookie(){
    let cookie = getCookie('userCookie')
    if (cookie == undefined){
        createUserCookie()
        var isCookie = false
    }
    else {
        var isCookie = true
    }
    return isCookie
}

function signInfunction(){
    $.ajax({
        url: "/auth/",
        method: 'POST',
        data: { 
            username: $('#Lemail').val(),
            password: $('#Lpassword').val()
            },
        contentType: 'application/x-www-form-urlencoded',
        crossDomain: true,
        success: function(a,b,c){
            var access_token = JSON.parse(c.responseText)
            access_token = access_token["access_token"]

            var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
            document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
            },
        error: function(e){}
        },)
}

function signUpfunction(){
    $.ajax({
        url: "/users/",
        method: 'POST',
        data: JSON.stringify({ 
            email: $('#Remail').val(),
            firstname: $('#Rfirstname').val(),
            lastname: $('#Rlastname').val(),
            password: $('#Rpassword').val()
            }),
        contentType: 'application/json',
        success: function(){
            
            },
        error: function(e){}
        },)
}

function checkAuth(){
    var isAuthorized = 
    $.ajax({
        url: "/auth/",
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+getCookie('auth')
        },
        success: function(a,b,c){
            console.log(a)
            console.log("użytkownik jest zalogowany!")
            return true
            },
        error: function(e){
            console.log("Zaloguj się!")
            return false
        }
        },)
    console.log(isAuthorized)
    return isAuthorized
}

async function load(){
    var res = await fetch(
        "/posts/",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer "+getCookie('auth')
            },
        }
    )
    res=await res.json()
    console.log(res)
}