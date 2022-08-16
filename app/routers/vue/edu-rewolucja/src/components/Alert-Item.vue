<template>
    <div v-if="show" class="alert">
        <div @click="closeAlert" class="alertcancel">X</div>
        <div class="textdetails">
            {{ text }}
        </div>
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
    text-align: center;
    color: white;
    width: 100%;
    background-color: #FF6E6E;
    height: 28px;
    padding: 0;
    margin: 0;
}
.textdetails{
    padding: 4px;
    text-align: center;
    width: 90%;
    margin-right: auto;
    margin-left: auto;
    transform: translateY(-28px);
}
.alertcancel{
    text-align: right;
    padding: 6px;
    cursor: pointer;
}
@media only screen and (max-width: 540px) {
  .alert{
    height: 47px;
  }
}
</style>