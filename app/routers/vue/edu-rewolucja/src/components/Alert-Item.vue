<template>
    <div v-if="show" class="alert">
        <div class="textdetails">
            Strona w trakcie budowy. Nie wszystko może działać poprawnie :(
        </div>
        <div @click="closeAlert" class="alertcancel">X</div>
    </div>
    <br v-if="show">
</template>

<script>
export default {
    // props: ['isAuthenticated', 'userData'],
    data() {
        return {
            show: false // zmień na true gdy naprawisz ;)
        }
    },
    methods: {
        closeAlert() {
            this.show = false
        },
}
}
</script>

<style>
.alert{
    position:absolute;
    top:35px;
    text-align: center;
    color: white;
    width: 100%;
    margin: 0;
}
.textdetails{
    background-color: #FF6E6E;
    float: left;
    padding: 4px;
    text-align: center;
    width: 100%;
}
.alertcancel{
    text-align: right;
    padding: 6px;
    transform: translateY(-22px);
    cursor: pointer;
}
</style>