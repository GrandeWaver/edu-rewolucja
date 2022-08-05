<template>
    <h1>Twoje zajęcia</h1>
    <!-- {{ $root.userData.account_type }} -->
    <br><br>
    <div v-if="no_classes">Brak zajęć</div>
    <div v-for="(class_, index) in classes" :key="class_.id" class="dashboard class">
        <div class="dashboard classWrapper">
            <img src="@/assets/icons8-more-64.png" class="dashboard more">
            <img :src=class_.picture class="dashboard picture">

            <div class="dashboard subject">{{ class_.subject }}</div>
            <div class="dashboard name">{{class_.firstname}} {{class_.lastname}}</div>
        </div>
        <div v-for="(schedule, schedule_index) in schedules[index]" :key="schedule_index" class="dashboard schedules"> 
            <div class="dashboard schedule">{{schedule.day}} {{schedule.hour}}</div>
        </div>
    </div>
</template>

<script>
import getData from '@/scripts/getData'
import nProgress from 'nprogress'

export default {
data(){
    return {
        no_classes: undefined,
        classes: [],
        schedules: [],
    }
},
mounted: async function () {
    nProgress.start()
    fetch(getData.url()+'/classes/', {
        headers: getData.getHeaders()
    })
    .then((response) => {
        if(response.status == 204){
            this.no_classes = true
            nProgress.done()
            return
        } if(response.status == 200){
            this.no_classes = false
            return response.json()
        }
        })
        .then((responseJSON) => {
            this.classes = responseJSON
            console.log(responseJSON)

            for (const e of this.classes){
                console.log(e)
                fetch(getData.url()+'/classes/schedules/'+e.id, {
                    headers: getData.getHeaders()
                })
                .then((response) => {
                    if(response.status == 204){
                        nProgress.done()
                        this.schedules.push([{day: 'Brak nadchodzących lekcji'}])
                        return
                    }
                    return response.json()
                })
                .then((responseJSON) => {
                    let new_data = []
                    if(responseJSON != undefined){
                        responseJSON.forEach(element => {
                            let new_element = JSON.parse(`{"day": "${element.day}", "hour": "${element.hour}:00"}`)
                            new_data.push(new_element)
                        });
                        this.schedules.push(new_data)
                        nProgress.done()
                    }
                })
                .catch((error) => {
                    alert(error)
                })
            }
        })
},
methods: {
}
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
    transform: translateX(8px);
}
.dashboard.more{
    float: right;
    height: 30px;
    transform: translateX(10px);
    opacity: 0.7;
}
.dashboard.more:hover{
    cursor: pointer;
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
</style>