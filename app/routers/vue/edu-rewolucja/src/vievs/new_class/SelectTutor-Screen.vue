<template>
<h1>Wybierz nauczyciela</h1>

<div v-if="!no_tutors" class="selectTutor wrapper">
    <div v-for="tutor in tutors" :key="tutor.tutor_id">
    <router-link :to="{ name: 'NewClass-date', params: { subject: subject}, query: { class_id: tutor.class_id } }">
        <div class="selectTutor tutor">
            
                <img :src=tutor.picture class="selectTutor picture">
                <div class="selectTutor details">
                    <div class="selectTutor detailsWrapper">
                        <div class="selectTutor name">{{ tutor.firstname }} {{ tutor.lastname }}</div>
                        <div class="selectTutor countLessons">lekcji: {{ tutor.lessons }}</div>
                        <div>{{ tutor.encoded }}</div>
                        <div class="selectTutor price">{{ tutor.price_netto }} zł</div>
                    </div>
                </div>
            
        </div>
        </router-link>
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
                } else if(r.status == 200){
                    no_tutors.value = false
                    return r.json()
                } else {
                    alert('Error: '+r.status);
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
                    nProgress.done()
                    })
                })
    })

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
.selectTutor.tutor{
    padding: 10px;
    height: 100px;
    margin-top: 20px;
}
.selectTutor.tutor:hover{
    background-color: rgba(204, 204, 204, 0.671);
}
.selectTutor.picture{
    margin: 10px;
    margin-right: 25px;
    float: left;
    border-radius: 50%;
    height: 100px;
    margin-top: auto;
    margin-bottom: auto;
}
.selectTutor.details{
    float: right;
    margin-left: auto;
    margin-right: auto;
    margin-top: auto;
    margin-bottom: auto;
    width: 255px;
    height: 100px;
}
.selectTutor.name{
    margin-bottom: 10px;
    font-size: larger;
    font-weight: 600;
}
.selectTutor.price{
    float: right;
    margin-top: 10px;
    opacity: 0.7;
}
.selectTutor.detailsWrapper{
    text-align: left;
    margin-top: auto;
    margin-bottom: auto;
}
.selectTutor.countLessons{
     margin-bottom: 10px;
}
@media only screen and (max-width: 440px) {
  .selectTutor.wrapper {
    width: 360px;
  }
  .selectTutor.price{
    float: left;
    display: block;
    opacity: 0.7;
    margin-top: 4px;
  }
  .selectTutor.details{
    width: 205px;
  }
  .selectTutor.countLessons{
    margin-bottom: 4px;
  }
  .selectTutor.name{
    margin-bottom: 4px;
  }
  .selectTutor.picture{
    margin: 6px;
    margin-right: 15px;
  }
}
@media not all and (min-resolution:.001dpcm) { 
  @supports (-webkit-appearance: none) {
    /* Safari Only CSS here */
    .selectTutor.details{
        transform: translateY(-5px);
    }
  }
}

</style>