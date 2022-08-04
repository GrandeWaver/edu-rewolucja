<template>
<div class="header">
    <router-link to="/" class="logo">edu-rewolucja</router-link>
    <!-- Gdy user nie jest zalogowany -->
    <div v-if="!isAuthenticated" class="right">
        <router-link :to="{ name: 'Login' }">Zaloguj się</router-link>
        <router-link :to="{ name: 'Register' }">Zarejestruj</router-link>
    </div>

    <!-- Gdy user jest zalogowany -->
    <div v-if="isAuthenticated" class="right">
        <a class="userinfo">id: {{ userData.id }} typ: {{ userData.account_type }} </a>
        <a @click="logout"> wyloguj</a>
        <!-- <img v-bind:src="'/users/picture/'+userData.id" height="40"> ta metoda nie wczytuje zdjęcia za pierwszym razem :/ -->
    </div>
</div>
</template>

<script>
import utils from '../scripts/utils'
import nProgress from 'nprogress';

export default {
    props: ['isAuthenticated', 'userData'],
    methods: {
        logout() {
            nProgress.start()
            utils.logoutFunc()
            this.$root.isAuthenticated = false
            this.$router.push({ name: 'Login', query: { redirect: '/login' } })
        },
}
}
</script>

<style>
.header{
    float: left;
    width: 100%;
    margin-left: 0;
    position:absolute;
    top:0;
    text-align: left;
}
.right{
    float: right;
    margin-right: 0;
    text-align: right;
    margin-top: 1vh;
}
.logo{
    font-size: 30px;
}
.userinfo{
    opacity: 0.5;
}
</style>