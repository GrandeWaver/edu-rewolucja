<template>
<div class="login wrapper">
    <div class="login container">
        <h1>Witaj z powrotem</h1>
        <div class="welcomeBack inline">
            <img :src=user_picture class="welcomeBack inline element photo">
            <h3 class="welcomeBack inline element user">{{ user }}</h3>
        </div>
        <div class="welcomeBack reset"></div>
        <br><br>
        <input type="password" placeholder="Hasło" v-model="input_password" v-on:keyup.enter="submit">
        <div v-if="alert" class="login redWarning">Podano nieprawidłowe hasło</div>
        <br><br>
        <button @click="submit">Dalej</button>
    </div>
</div>
</template>

<script>
import getData from '.././scripts/getData'
import nProgress from 'nprogress';
import auth from '.././scripts/auth';

export default {
    data(){
        return {
            user: this.$route.query.user,
            input_password: undefined,
            user_picture: "https://icon-library.com/images/unknown-person-icon/unknown-person-icon-9.jpg",
            alert: false
        }
    },
    mounted: function () {
        fetch(getData.url()+"/users/picture-from-email/"+this.user, {
            headers: {"Content-Type": "application/json",},
          })
            .then((response) => {
                    return response.json()
            })
            .then((responseJSON) => {
                    this.user_picture = getData.url()+responseJSON.picture
            })
            .catch((error) => {
                alert(error)
              })
    },
    methods: {
        submit () {
            if (this.input_password === undefined || String(this.input_password).length == 0){
                this.alert = true
            } else {
                nProgress.start()
                this.alert = false
                fetch(getData.url()+"/auth/", {
                method: "POST",
                dataType: "json",
                body: new URLSearchParams({
                    'username': this.user,
                    'password': this.input_password
                }),
                headers: {"Content-Type": "application/x-www-form-urlencoded",},
            })
                .then((response) => {
                    if(response.status == 422){
                        alert('Błąd wprowadzanych danych')
                        this.alert = false
                        nProgress.done()
                        return
                    } if(response.status == 403){
                        this.alert = true
                        nProgress.done()
                        return
                    } if(response.status == 200){
                        return response.json()
                    }
                })
                .then((responseJSON) => {
                    auth.createLoginCookie(responseJSON)
                })
            }
        }
    }
}
</script>

<style>
.welcomeBack.inline.element{
    float: left;
}
.welcomeBack.inline.element.photo{
    padding: 15px;
    padding-left: 0;
    height: 55px;
    width: 55;
}
.welcomeBack.inline.element.user{
    padding: 15px;
}
.welcomeBack.inline{
    overflow: auto;
}
.welcomeBack.reset{
    display: block;
}
@media only screen and (max-width: 440px) {
    .welcomeBack.inline.element.user{
        padding-top: 20px;
        font-size: medium;
    }
  .login.wrapper {
    width: 360px;
  }
}
</style>