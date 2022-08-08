<template>
<h1 v-if="$root.userData.account_type == 'student'">Czego chcesz się uczyć?</h1>


<div class="selectClass wrapper">
    <router-link :to="{ name: 'NewClass-tutor', params: { subject: 'matematyka' } }">
        <div class="selectClass subject">
            <img src="@/assets/icons8-calculator-64.png" class="selectClass icon">
            <div class="selectClass details">matematyka</div>
        </div>
    </router-link>
    <router-link :to="{ name: 'NewClass-tutor', params: { subject: 'angielski' } }">
        <div class="selectClass subject">
                <img src="@/assets/icons8-book-64.png" class="selectClass icon">
            <div class="selectClass details">angielski</div>
        </div>
    </router-link>
    
    <StrikeItem text="wkrótce" />

    <div class="selectClass subject unavailable">
            <img src="@/assets/icons8-source-code-50.png" class="selectClass icon">
        <div class="selectClass details">python</div>
    </div>
    <div class="selectClass subject unavailable">
            <img src="@/assets/icons8-book-64.png" class="selectClass icon">
        <div class="selectClass details">hiszpański</div>
    </div>
    <div class="selectClass subject unavailable">
            <img src="@/assets/icons8-atom-64.png" class="selectClass icon">
        <div class="selectClass details">chemia</div>
    </div>

    <div style="display:initial"></div>

</div>





<h1 v-if="$root.userData.account_type == 'tutor'">Czego chcesz uczyć?</h1>
</template>

<script>
import StrikeItem from '../../components/Strike-Item.vue'
export default{
components: {
    StrikeItem
}
}

</script>

<style>
.selectClass.wrapper{
    margin-top: 20px;
    height: 445px;
    width: 410px;
    margin-left: auto;
    margin-right: auto;

    border-radius: 16px;
    border: 1px solid #ccc;
}
@media only screen and (max-width: 440px) {
  .selectClass.wrapper {
    width: 360px;
    height: 445px;
  }
}
.selectClass.subject{
    width: 100%;
    text-align: left;
}
.selectClass.subject:hover{
    background-color: #ccc;
}
.selectClass.icon{
    height: 50px;
    padding: 10px;
    padding-right: 25px;
    float: left;
}
.selectClass.details{
    padding: 25px;
    font-size: larger;
}
.unavailable{
    opacity: 0.5;
}
.selectClass.subject.unavailable:hover{
    background-color: rgba(255, 255, 255, 0);
}
</style>