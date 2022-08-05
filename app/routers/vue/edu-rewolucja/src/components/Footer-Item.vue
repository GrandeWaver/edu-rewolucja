<template>
    <footer>
        <router-link :to="{ name: 'RegisterTutor' }">Zostań korepetytorem</router-link>
        <router-link :to="{ name: 'Contact' }">Kontakt</router-link>
        <router-link :to="{ name: 'PrivacyPolicy' }">Polityka Prywatności</router-link>
        <router-link :to="{ name: 'TermsAndConditions' }">Watunki korzystania z aplikacji</router-link>
    </footer>
</template>

<style>
footer {
    height:20px;
    width:100%;
}
</style>