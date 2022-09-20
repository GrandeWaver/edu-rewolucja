<template>
    <div v-if="show" class="alert">
        <div class="textdetails">
            {{ text }}
        </div>
        <div @click="closeAlert" class="alertcancel pointer">X</div>
    </div>
</template>

<script>
export default {
    props: ['text'],
    data() {
        return {
            show: true // zmień na true gdy naprawisz ;)
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
    color: white;
    width: 100%;
    background-color: #FF6E6E;
    padding: 0;
    margin: 0;
}
.textdetails{
    padding: 4px;
    text-align: center;
    width: 90%;
    margin-right: auto;
    margin-left: auto;
    display:inline-block;
}
.alertcancel{
    padding: 6px;
    width: 1%;
    cursor: pointer;
    display:inline-block;
    vertical-align:top;
    text-align: right;
}
@media only screen and (min-width: 1000px) {
.textdetails {
    width: 95%;
}
}
@media only screen and (min-width: 1600px) {
.textdetails {
    width: 97%;
}
}
</style>