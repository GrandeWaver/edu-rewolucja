<template>
<div class="login wrapper">
    <div class="login container">
        <h1>Zaloguj się</h1>
        Nowy użytkownik? 
        <router-link :to="{ name: 'Register' }">Utwórz konto</router-link>
        
        <br><br>
        <div class="login google">Kontynuuj z Google</div>
        <br>

        <GoogleLogin :callback="handleResponse"/>

        <!-- <br><br><br>
        <div class="strike"><span>Lub</span></div>
        <br><br>
        
        <div id="app" v-cloak>
        Email:<input :value="userData.email" v-on:keyup.enter="checkEmailFunc()" type="email" id="Cemail" placeholder="example@gmail.com"><br><br>
        <div v-if="val.notValidCEmail1" class="redWarning">
            Nie możemy znaleźć konta z takim adresem email
            <a href="/signup" class="blueWarning">Stwórz nowe konto</a>
        </div><! Błąd emaila
        <div v-if="val.notValidCEmail2" class="redWarning">Podano nieprawidłowy email</div> Błąd emaila 
        <button @click="checkEmailFunc()" id="checkEmail" type="submit">Dalej</button>
        </div> -->
    </div>
</div>
</template>

<script>
import nProgress from 'nprogress';
import callback from '../scripts/google-signin'

export default {
    methods: {
        handleResponse(response){
            nProgress.start()
            callback(response, this)
        }
    }
}
</script>

<style>
.login.wrapper{
    background-color: beige;
    width: 400px;
    margin-left: auto;
    margin-right: auto;
    text-align: left;
}
.login.container{
    padding: 20px;
    padding-top: 5px;
}
.login.google{
    opacity: 0.55;
}
</style>