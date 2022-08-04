import cookies from "./cookies"

const headersAuth = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+cookies.getCookie('auth')
  }

  var getData = {
    url(){
        if (window.location.hostname == 'localhost'){
            return 'http://localhost:3000'
        } if (window.location.hostname == 'korki.edu-rewolucja.pl'){
            return 'https://app.edu-rewolucja.pl'
        }
    },

    async getData(_this, url = ''){
        const response = await fetch(url, {
        dataType: "json",
        headers: headersAuth,
        })
        if(response.status == 204){
            return response
        }
        return response.json()
    }
  }

  export default getData