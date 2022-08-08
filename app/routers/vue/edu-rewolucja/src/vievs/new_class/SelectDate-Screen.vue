<template>
<h1>Wybierz datę lekcji</h1>
<div v-if="available_schedules.length != 0" class="buyLesson wrapper">
    
    <div class="buyLesson miniheader">
        <img src="@/assets/casual-life-3d-clock-with-blue-arrow.png" class="buyLesson clock">
        <div class="buyLesson subject">{{ subject }}</div>
        {{ available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].full_name }},
        {{ select_first_lesson.day }}
        {{ select_first_lesson.month }}
        {{ select_first_lesson.hour }}:00-{{ select_first_lesson.hour }}:55
    </div>

    <br><br>
    <StrikeItem text="wybierz datę" />
    <br><br>

    <div class="buyLesson select">
        <select v-model="select_first_lesson.day_index" 
            @change="
            select_first_lesson.day = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].day;
            select_first_lesson.hour = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].working_hours[select_first_lesson.hour_index].hour">
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
                select_first_lesson.hour = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].working_hours[select_first_lesson.hour_index].hour
            ">
            <option v-for="month in available_schedules" v-bind:value="month.month_index" :key="month.month_index">{{month.month}}</option>
        </select>
        <select v-model="select_first_lesson.hour_index" 
        @change="select_first_lesson.hour = available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].working_hours[select_first_lesson.hour_index].hour">
            <option 
                v-for="hour in available_schedules[select_first_lesson.month_index].days[select_first_lesson.day_index].working_hours" 
                v-bind:value="hour.id" :key="hour.id">{{hour.hour}}:00
            </option>
        </select>
        </div>
        <button @click="submit" class="submit">Zapisz</button>
</div>
</template>

<script>
import getData from '../../scripts/getData'
import nProgress from 'nprogress'
import StrikeItem from '../../components/Strike-Item.vue'

export default {
    props: ['class_id', 'subject'],
    components: {
        StrikeItem
    },
    data () {
        return {
            available_schedules: [],
            select_first_lesson: {day: undefined, month: undefined, month_index: 0, day_index: 0, hour_index: 0, hour: undefined},
        }
    },
    mounted: function () {
        if(this.class_id == undefined || this.subject == undefined){
            alert('Przerwanie tworzenia zajęć. \nNastąpi przekierowanie do panelu')
            this.$router.push({name: 'Dashboard'})
        }
        nProgress.start()
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
                this.select_first_lesson.hour = responseJSON[this.select_first_lesson.month_index].days[this.select_first_lesson.day_index].working_hours[this.select_first_lesson.hour_index].hour
            })
    },
    methods: {
        submit () {
            nProgress.start()
            fetch(getData.url()+"/create_class/student", {
                method: "POST",
                dataType: "json",
                body: JSON.stringify({
                available_class_id: this.class_id,
                month: this.select_first_lesson.month,
                year: this.select_first_lesson.year,
                day_name: this.available_schedules[this.select_first_lesson.month_index].days[this.select_first_lesson.day_index].name,
                day: this.select_first_lesson.day,
                hour: this.select_first_lesson.hour,
                }),
                headers: getData.getHeaders()
            })
            .then(response => {
                if(response.status == 201){
                    this.$router.push({ name: 'Dashboard' })
                } if(response.status == 500){
                alert('error: błąd połączenia z bazą danych... \nkod błędu: 500')
                } if(response.status == 409){
                    nProgress.done()
                    alert('Masz już zajęcia tego przedmiotu z tym nauczycielem. \nNastąpi przekierowanie do panelu')
                    this.$router.push({name: 'Dashboard'})
                }
            })
            nProgress.done()
        },
    },
}
</script>