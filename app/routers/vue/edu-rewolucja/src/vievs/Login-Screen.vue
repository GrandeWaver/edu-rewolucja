<template>
<div class="login wrapper">
    <div class="login container">
        <h1>Zaloguj się</h1>
        Nowy użytkownik? 
        <router-link :to="{ name: 'Register' }">Utwórz konto</router-link>
        
        <br><br>
        <div class="login opacity">Kontynuuj z Google</div>
        <br>

        <GoogleLogin :callback="handleResponse"/>

        <br><br><br>
        <StrikeItem text="Lub" />
        <br><br>
        <div class="login opacity">Zaloguj przy użyciu email</div>
        <br>
        
        <input type="email" placeholder="example@gmail.com" v-model="input_email" v-on:keyup.enter="submit">
        <div v-if="alert0" class="login redWarning">Puste pole</div>
        <div v-if="alert1" class="login redWarning">
            Nie możemy znaleźć konta z takim adresem email.
            <router-link class="login blueWarning login a" :to="{ name: 'Register' }">Stwórz nowe konto</router-link>
        </div>
        <div v-if="alert2" class="login redWarning">Podano nieprawidłowy email</div>
        <br><br>
        <button @click="submit">Dalej</button>
    </div>
</div>
</template>

<script>
import nProgress from 'nprogress';
import callback from '../scripts/google-signin'
import StrikeItem from '../components/Strike-Item.vue';
import getData from '@/scripts/getData';

export default {
    components: {
    StrikeItem
},
    data (){
        return {
            input_email: undefined,
            alert0: false,
            alert1: false,
            alert2: false
        }
    },
    methods: {
        handleResponse(response){
            nProgress.start()
            callback(response, this)
        },
        submit(){
            if (this.input_email === undefined || String(this.input_email).length == 0){
                this.alert0 = true
                this.alert1 = false
                this.alert2 = false
            } else {
                nProgress.start()
                this.alert0 = false
                fetch(getData.url()+"/users/check", {
                method: "POST",
                dataType: "json",
                body: JSON.stringify({email: this.input_email}),
                headers: {"Content-Type": "application/json",},
            })
                .then((response) => {
                    if(response.status == 422){
                        this.alert2 = true
                        nProgress.done()
                        return
                    } if(response.status == 200){
                        this.alert2 = false
                        return response.json()
                    }
                })
                .then((responseJSON) => {
                    if (responseJSON.response == 'false'){
                        this.alert1 = true
                        nProgress.done()
                    } if (responseJSON.response == 'true'){
                        this.alert1 = false
                        nProgress.done()
                        this.$router.push({ name: 'WelcomeBack', query: { user: this.input_email } })
                    }
                })
            }
        }
    }
}
</script>

<style>
.login.wrapper{
    margin-top: 20px;
    width: 410px;
    margin-left: auto;
    margin-right: auto;
    text-align: left;

    border-radius: 16px;
    border: 1px solid #ccc;
}
@media only screen and (max-width: 440px) {
  .login.wrapper {
    width: 360px;
  }
}
.login.container{
    padding: 20px;
    padding-top: 5px;
    padding-bottom: 50px;
}
.login.opacity{
    opacity: 0.55;
}
.login.a{
    padding: 0px;
}
.login.redWarning{
    padding-top: 5px;
    padding-bottom: 5px;
    color: rgb(255, 55, 55);
}
.login.blueWarning{
    color: rgb(49, 49, 255);
}
</style>