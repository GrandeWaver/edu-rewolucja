import getData from "./getData"
import nProgress from 'nprogress';

const callback = (response, _this) => {
    // This callback will be triggered when the user selects or login to
    // his Google account from the popup

        // $.ajax({
        //     url: "/auth/googleuser",
        //     method: 'POST',
        //     data: JSON.stringify({ 
        //     token: response.credential,
        //         }),
        //         headers: {
        //             "Content-Type": "application/json",
        //         },
        //     success: function(a, b, c){
        //     var access_token = JSON.parse(c.responseText)
        //     access_token = access_token["access_token"]

        //     var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
        //     document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
        //     window.location.href = '/'
        //         },
        //     error: function(e){
        //     alert(e.responseJSON.detail)
        //     }
        //     },)
        // }

        fetch(getData.url()+"/auth/googleuser", {
            method: "POST",
            dataType: "json",
            body: JSON.stringify({token: response.credential}),
            headers: {"Content-Type": "application/json",},
          })
            .then((response) => {
                if(response.status == 400){
                    nProgress.done()
                    alert('Zaloguj się przez email, a nie przez Google')
                    return
                } if(response.status == 200){
                    return response.json()
                }
            })
            .then((responseJSON) => {
                if (responseJSON != undefined){
                    let access_token = responseJSON.access_token
                    var expire_date = new Date(new Date().getTime()+60*60*1000*720).toGMTString(); // 720h
                    document.cookie = "auth="+access_token+"; expires="+expire_date+"; path=/";
                    // location.reload();
                    _this.$root.isAuthenticated = true
                    _this.$router.push({ name: 'Dashboard' })
                }
            })
            .catch((error) => {
                alert(error)
              })
  }

  export default callback