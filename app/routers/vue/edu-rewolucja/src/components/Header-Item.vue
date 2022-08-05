<template>
<div class="header">
    <router-link to="/" class="logo">edu-rewolucja</router-link>
    <!-- Gdy user nie jest zalogowany -->
    <div v-if="!isAuthenticated" class="right">
        <div class="right unauthorized">
            <router-link :to="{ name: 'Login' }">Zaloguj się</router-link>
            <router-link :to="{ name: 'Register' }">Zarejestruj</router-link>
        </div>
    </div>

    <!-- Gdy user jest zalogowany -->
    <div v-if="isAuthenticated" class="right">
    <div class="user container">
        <a class="user info">id: {{ userData.id }} typ: {{ userData.account_type }}</a>
        <a @click="logout"> wyloguj</a>
    </div>
    <div>
        <img :src=userData.picture class="user picture">
    </div>
    </div>
</div>
</template>

<script>
import auth from '../scripts/auth'
import nProgress from 'nprogress';

export default {
    props: ['isAuthenticated', 'userData'],
    methods: {
        logout() {
            nProgress.start()
            auth.logoutFunc()
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
    text-align: right;
}
.right > div{
    display: table-cell;
}
.right.unauthorized{
    padding: 10px;
}
.logo{
    font-size: 30px;
}
.user.container {
    position: relative;
    top: -25px;
}
.user.info{
    opacity: 0.5;
}
@media only screen and (max-width: 500px) {
    .logo{
        margin-top: 5px;
        margin-left: 5px;
    }
  .user.info {
    display: none;
  }
  .right.unauthorized {
    display: none;
  }
}
.user.picture{
    margin: 5px;
    height: 40px;
    border-radius: 50%;
}
</style>