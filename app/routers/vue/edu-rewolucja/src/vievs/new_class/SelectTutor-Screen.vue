<template>
<h1>Wybierz nauczyciela</h1>

<div v-if="!no_tutors" class="selectTutor wrapper">
    <div v-for="tutor in tutors" :key="tutor.tutor_id">
        <div class="selectTutor tutor">
            <router-link :to="{ name: 'NewClass-date', params: { class_id: tutor.class_id, subject: subject} }">
                <img :src=tutor.picture class="selectTutor picture">
                <div class="selectTutor details">
                    <div class="selectTutor price">50 zł</div>
                    <div class="selectTutor name">{{ tutor.firstname }} {{ tutor.lastname }}</div>
                    <!-- <div>lekcji: 0</div> -->
                    <div>{{ tutor.encoded }}</div>
                </div>
            </router-link>
        </div>
    </div>
    <br>
</div>

<div v-if="no_tutors">Brak dostępnych nauczycieli</div>

</template>

<script>
import getData from '../../scripts/getData'
import { onMounted, ref  } from "vue";
import nProgress from 'nprogress';
import utils from '../../scripts/utils'

export default {
    props: ['subject'],
    setup(props) {
    nProgress.start()
    const tutors = ref([])
    const no_tutors = ref(null)
    
    onMounted(async () => {
        fetch(getData.url()+'/select_class/'+props.subject, {headers: getData.getHeaders()})
            .then(r => {
                if(r.status == 204){
                    no_tutors.value = true
                    nProgress.done()
                    return
                } if(r.status == 200){
                    no_tutors.value = false
                    return r.json()
                }
            })
            .then(data => {
                tutors.value = data
                tutors.value.forEach(function (value, index) {
                    let encoded = utils.encodeRank(tutors.value[index].rank)
                    tutors.value[index].encoded = encoded

                    let picture = value.picture
                    if(!picture.startsWith('https://')){
                        tutors.value[index].picture = getData.url()+picture
                        }
                    })
                })
    })
    nProgress.done()

    return { tutors, no_tutors };
  },
}
</script>

<style>
.selectTutor.wrapper{
    margin-top: 20px;
    width: 410px;
    margin-left: auto;
    margin-right: auto;
    text-align: left;
    

    border-radius: 16px;
    border: 1px solid #ccc;
}
@media only screen and (max-width: 440px) {
  .selectTutor.wrapper {
    width: 360px;
  }
}
.selectTutor.tutor{
    padding: 20px;
    padding-top: 10px;
    height: fit-content;
    margin-top: 20px;
}
.selectTutor.tutor:hover{
    background-color: rgba(204, 204, 204, 0.671);
}
.selectTutor.picture{
    padding: 10px;
    margin-right: 25px;
    float: left;
    border-radius: 50%;
    height: 90px;
    transform: translateY(-12px);
}
.selectTutor.details{
    display: block;
}
.selectTutor.name{
    margin-bottom: 10px;
    font-size: larger;
    font-weight: 600;
}
.selectTutor.price{
    float: right;
    opacity: 0.7;
}

</style>