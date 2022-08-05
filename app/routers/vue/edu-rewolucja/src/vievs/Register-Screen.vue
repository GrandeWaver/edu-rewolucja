<template>
<div class="login wrapper">
    <div class="login container">
        <h1>Załóż konto</h1>
        Masz już konto?
        <router-link :to="{ name: 'Login' }" class="textcolor blue">Zaloguj się</router-link>
        
        <br><br>
        <div class="login opacity">Zarejestruj się z Google</div>
        <br>

        <GoogleLogin :callback="handleResponse"/>

        <br><br><br>
        <StrikeItem text="Lub" />
        <br><br>
        <div class="login opacity">Zarejestruj się przez email</div>
        <br>

        <input type="email" placeholder="example@gmail.com" v-model="input_email" v-on:keyup.enter="submit" class="register input">
        <div v-if="alert.email0" class="login redWarning">Puste pole</div>
        <div v-if="alert.email1" class="login redWarning">
            Użytkownik z takim adresem email już istnieje.
            <router-link class="login blueWarning login a" :to="{ name: 'Login' }">Zaloguj się</router-link>
        </div>
        <div v-if="alert.email2" class="login redWarning">Podano nieprawidłowy email</div>

        <input type="text" placeholder="imię" v-model="input_firstname" v-on:keyup.enter="submit" class="register input">
        <div v-if="alert.firstname0" class="login redWarning">Puste pole</div>

        <input type="text" placeholder="nazwisko" v-model="input_lastname" v-on:keyup.enter="submit" class="register input">
        <div v-if="alert.lastname0" class="login redWarning">Puste pole</div>
        
        <div class="register inline">
            <span class="register left">
                <input v-if="showPassword" type="text" placeholder="hasło" v-model="input_password" v-on:keyup.enter="submit" class="register input password">
                <input v-else type="password" placeholder="hasło" v-model="input_password" v-on:keyup.enter="submit" class="register input password">
            </span>
            <span v-if="!showPassword" @click="toggleShow" class="register right"><img src="@/assets/icons8-eye-48.png" class="register eye"></span>
            <span v-else @click="toggleShow" class="register right"><img src="@/assets/icons8-closed-eye-32.png" class="register eye"></span>
        </div>

        <div v-if="alert.password0" class="login redWarning">Puste pole</div>
        <div v-if="alert.password1" class="login redWarning">Za krótkie hasło</div>

        <br><br>
        <button @click="submit">Załóż konto</button>
    </div>
</div>
</template>

<script>
import nProgress from 'nprogress';
import StrikeItem from '../components/Strike-Item.vue';
import callback from '../scripts/google-signin'
import utils from '../scripts/utils'
import getData from '../scripts/getData';

export default {
    components: {
    StrikeItem
},
data () {
    return {
        input_email: undefined,
        input_firstname: undefined,
        input_lastname: undefined,
        input_password: undefined,
        alert: [],

        showPassword: false,
    }
},
methods: {
    handleResponse(response){
        nProgress.start()
        callback(response, this)
        },
    showPasswordFF(){
        var x = document.getElementsByClassName("register input password");
        console.log(x.type)
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    },
    submit () {
        // alert('Sorki, sorki ale to jeszcze nie działa... \nSprawdź jutro :)')
        if (utils.isBlankVal(this.input_email)){
            this.alert.email0 = true
            this.alert.email1 = false
            this.alert.email2 = false
        } else {
            this.alert.email0 = false
        } if (utils.isBlankVal(this.input_firstname)){
            this.alert.firstname0 = true
        } else {
            this.alert.firstname0 = false
        } if (utils.isBlankVal(this.input_lastname)){
            this.alert.lastname0 = true
        } else {
            this.alert.lastname0 = false
        } if (utils.isBlankVal(this.input_password)){
            this.alert.password0 = true
            this.alert.password1 = false
        } else {
            this.alert.password0 = false
        }

        if(!utils.isBlankVal(this.input_email) && !utils.isBlankVal(this.input_firstname) && !utils.isBlankVal(this.input_lastname) && !utils.isBlankVal(this.input_password)) {
                nProgress.start()
                this.alert0 = false
                fetch(getData.url()+"/users/", {
                method: "POST",
                dataType: "json",
                body: JSON.stringify({
                  email: this.input_email,
                  firstname: this.input_firstname,
                  lastname: this.input_lastname,
                  password: this.input_password
                    }),
                headers: {"Content-Type": "application/json",},
            })
                .then((response) => {
                    nProgress.done()
                    if (response.status == 201){
                        this.$router.push({ name: 'Login'})
                        return response.json()
                    } else {
                        return response.json()
                    }
                })
                .then((responseJSON) => {
                    if (Array.isArray(responseJSON.detail)){
                        if(responseJSON.detail[0].msg == 'value is not a valid email address'){
                            this.alert.email1 = false
                            this.alert.email2 = true
                            this.alert.password1 = false
                        }
                    } if (responseJSON.detail == 'User already exists') {
                        this.alert.email1 = true
                        this.alert.email2 = false
                        this.alert.password1 = false
                    } if (responseJSON.detail == 'Password is too short') {
                        this.alert.email1 = false
                        this.alert.email2 = false
                        this.alert.password1 = true
                    }
                })
                .catch((error) => {
                    alert(error)
              })
            }
    },
    toggleShow() {
      this.showPassword = !this.showPassword;
    }
},
  computed: {
    buttonLabel() {
      return (this.showPassword) ? "Hide" : "Show";
    }
  },
}
</script>

<style>
.register.input {
    margin-top: 10px;
    margin-bottom: 10px;
}
.register.input.password{
    width: 100%;
}
.register.right{
    opacity: 0.55;
    transform: translateY(-37px)
}
.register.eye{
    height: 20px;
}
</style>