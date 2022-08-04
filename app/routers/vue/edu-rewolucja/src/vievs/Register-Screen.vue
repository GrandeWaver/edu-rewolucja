<template>
<div class="login wrapper">
    <div class="login container">
        <h1>Załóż konto</h1>
        Masz już konto?
        <router-link :to="{ name: 'Login' }">Zaloguj się</router-link>
        
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
        <input type="text" placeholder="imię" v-model="input_email" v-on:keyup.enter="submit" class="register input">
        <input type="text" placeholder="nazwisko" v-model="input_email" v-on:keyup.enter="submit" class="register input">
        <input type="password" placeholder="hasło" v-model="input_email" v-on:keyup.enter="submit" class="register input">
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
import StrikeItem from '../components/Strike-Item.vue';
import callback from '../scripts/google-signin'

export default {
    components: {
    StrikeItem
},
methods: {
    handleResponse(response){
        nProgress.start()
        callback(response, this)
        },
    submit () {
        alert('Sorki, sorki ale to jeszcze nie działa... \nSprawdź jutro :)')
    }
}
}
</script>

<style>
.register.input {
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>