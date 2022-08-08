<template>
<h1>Zaplanuj lekcje</h1>

<div v-if="available_schedules.length != 0" class="buyLesson wrapper">
    
    <div class="buyLesson miniheader">
        <img src="@/assets/casual-life-3d-clock-with-blue-arrow.png" class="buyLesson clock">
        <div class="buyLesson subject">{{ subject }}</div>
        dzień tygodnia: {{available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].name}}
    </div>

    <br><br>
    <StrikeItem text="wybierz datę" />
    <br><br>

    <div class="buyLesson select">
        <select v-model="select_first_lesson.day_index" 
            @change="select_first_lesson.day = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].day">
            <option 
                v-for="day in available_schedules[select_first_lesson.month_index].days" 
                v-bind:value="day.day_index" :key="day.day_index">
                {{day.day}}
            </option>
        </select>
        <select v-model="select_first_lesson.month_index" 
            @change="
                select_first_lesson.day_index = 0; 
                select_first_lesson.month = available_schedules[select_first_lesson.month_index].month
                select_first_lesson.day = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].day
                select_first_lesson.year = available_schedules[select_first_lesson.month_index].year
            ">
            <option v-for="month in available_schedules" v-bind:value="month.month_index" :key="month.month_index">{{month.month}}</option>
        </select>
        <select v-model="select_first_lesson.hour" id="select_hour_buy">
            <option 
                v-for="( hour, hour_index ) in available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].working_hours" 
                v-bind:value="hour" :key="hour_index">{{hour}}:00
            </option>
        </select>
        </div>
        <button @click="submit" class="submit">Zapisz</button>
</div>
</template>

<script>
import getData from '../scripts/getData'
import nProgress from 'nprogress'
import StrikeItem from '../components/Strike-Item.vue'

export default {
    props: ['id'],
    components: {
        StrikeItem
    },
    data () {
        return {
            class_id: undefined,
            subject: undefined,
            available_schedules: [],
            select_first_lesson: {day: undefined, month: undefined, month_index: 0, day_index: 0, hour: undefined},
        }
    },
    mounted: function () {
        nProgress.start()
        fetch(getData.url()+"/lesson/get-available-class-id/"+this.id, {
            headers: getData.getHeaders()
        })
        .then((response) => {
            return response.json()
        })
        .then((responseJSON) => {
            this.class_id = responseJSON.source_available_class_id
            this.subject = responseJSON.subject
            fetch(getData.url()+"/select_class/schedules/"+this.class_id, {
                headers: getData.getHeaders()
            })
            .then((response) => {
                return response.json()
            })
            .then((responseJSON) => {
                nProgress.done()
                this.available_schedules = responseJSON
                this.select_first_lesson.day = responseJSON[this.select_first_lesson.month_index].days[this.select_first_lesson.day_index].day
                this.select_first_lesson.month = responseJSON[this.select_first_lesson.month_index].month
                this.select_first_lesson.year = responseJSON[this.select_first_lesson.month_index].year
            })
        })
    },
    methods: {
        submit () {
            nProgress.start()
            fetch(getData.url()+"/lesson/", {
                method: "POST",
                dataType: "json",
                body: JSON.stringify({
                month: this.select_first_lesson.month,
                year: this.select_first_lesson.year,
                day_name: this.available_schedules[this.select_first_lesson.month_index].days[this.select_first_lesson.day_index].name,
                day: this.select_first_lesson.day,
                hour: this.select_first_lesson.hour,
                class_id: this.id
                }),
                headers: getData.getHeaders()
            })
            .then(response => {
                if(response.status == 201){
                    this.$router.push({ name: 'Dashboard' })
                }
                if(response.status == 500){
                alert('error: błąd połączenia z bazą danych... \nkod błędu: 500')
                }
            })
            nProgress.done()
        }
    }
}
</script>

<style>
.buyLesson.wrapper{
    margin-top: 20px;
    height: 330px;
    width: 410px;
    margin-left: auto;
    margin-right: auto;

    border-radius: 16px;
    border: 1px solid #ccc;
}
@media only screen and (max-width: 440px) {
  .buyLesson.wrapper {
    width: 360px;
    height: 330px;
  }
}
.buyLesson.clock {
    float: left;
    width: 100px;
    padding-left: 15px;
    padding-right: 20px;
}
.buyLesson.miniheader{
    text-align: left;
    padding: 20px;
}
.buyLesson.subject{
    margin-top: 15px;
    padding-bottom: 10px;
    font-weight: 600;
    font-size: medium;
}
.buyLesson.select{
    margin-bottom: 40px;
}
.submit{
    margin-left: auto;
    margin-right: auto;
    float: initial;
    background-color: #FF6E6E;
    color: white;
    border-radius: 10px;
    font-size: medium;
}
.submit:hover{
    background-color: #ff5252;
}
</style>