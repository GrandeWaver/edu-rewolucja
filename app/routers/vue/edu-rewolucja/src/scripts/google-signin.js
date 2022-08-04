import getData from "./getData"
import nProgress from 'nprogress';
import auth from './auth'

async function callback (response){
    // This callback will be triggered when the user selects or login to
    // his Google account from the popup

        await fetch(getData.url()+"/auth/googleuser", {
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
                    auth.createLoginCookie(responseJSON)
                }
            })
            .catch((error) => {
                alert(error)
              })
  }

  export default callback