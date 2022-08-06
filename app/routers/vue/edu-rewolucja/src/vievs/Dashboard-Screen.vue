

<template>
    <!-- {{ $root.userData.account_type }} -->
     <h1>Twoje zajęcia</h1>

     <br><br>
    <div v-if="no_classes">Brak zajęć</div>
    <div v-for="class_ in classes" :key="class_.id" class="dashboard class">
        <div class="dashboard classWrapper">
            <img :src=class_.picture class="dashboard picture">

            <div class="dashboard subject">{{ class_.subject }}</div>
            <div class="dashboard name">{{class_.firstname}} {{class_.lastname}}</div>
        </div>
        <div v-for="(schedule, schedule_index) in class_.schedules" :key="schedule_index" class="dashboard schedules"> 
            <div class="dashboard schedule">{{schedule.day}} {{schedule.hour}}</div>
        </div>
        <div class="dashboard buyLesson">
            <router-link :to="{ name: 'BuyLesson', params: { id: class_.id } }" class="textcolor blue">Zaplanuj lekcje</router-link>
        </div>
    </div>
 </template>
<script>
import getData from '../scripts/getData'
import { onMounted, ref } from "vue";
import nProgress from 'nprogress';

export default {
setup() {
    nProgress.start()
    const classes = ref([])
    const no_classes = ref(null)
    
    onMounted(async () => {
        fetch(getData.url()+'/classes/get-classses', {headers: getData.getHeaders()})
            .then(r => {
                if(r.status == 204){
                    no_classes.value = true
                    nProgress.done()
                    return
                } if(r.status == 200){
                    no_classes.value = false
                    return r.json()
                }
            })
            .then(data => {classes.value = data})
    })
    nProgress.done()
    return { classes, no_classes };
  },
 }

</script>

<style>
.dashboard.class{
    width: 500px;
    margin-left: auto;
    margin-right: auto;
    text-align: left;
    padding-bottom: 10px;

    border-radius: 16px;
    border: 1px solid #ccc;

    margin-bottom: 50px;
}
@media only screen and (max-width: 440px) {
  .dashboard.class{
    width: 300px;
  }
}
.dashboard.classWrapper{
    padding: 10px;

    border-radius: 16px;
    border: 1px solid #ccc;
    background-color: rgb(9, 131, 80);
    color: white;
}
.dashboard.picture{
    float: right;
    height: 80px;
    border-radius: 50%;
    /* transform: translateX(-px); */
}
.dashboard.subject{
    font-size: larger;
    font-weight: 600;
    padding-bottom: 10px;
}
.dashboard.name{
    padding-bottom: 30px;
}
.dashboard.schedules {
    margin-top: 8px;
    padding: 10px;
}
.dashboard.buyLesson {
    margin: 10px;
    margin-left: 5px;
}
</style>