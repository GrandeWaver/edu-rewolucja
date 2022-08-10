<template>
<h1>W jakie dni chcesz mieć zajęcia?</h1>

<div class="wrapper selectSchedule">
    <div class="selectSchedule mini-wrapper">
        <div v-for="(day, index) in days" :key="index">
            <div @click="selectDay(day, index)">
                <div class="selectSchedule day" :class="changeClass(index)">{{ day }}</div>
            </div>
        </div>
    </div>

    <div class="selectSchedule mini-wrapper-two">
        <img @click="dayBack" src="@/assets/icons8-back-50.png" class="selectSchedule arrow">
            <div class="selectSchedule currentDay-wrapper">
                <span class="selectSchedule currentDay">{{ availability[selected_day][0].name }} </span>
            </div>
        <img @click="dayUp" src="@/assets/icons8-forward-50.png" class="selectSchedule arrow">
    </div>

    <StrikeItem text="godziny dostępności" />

    <br>
    <div class="padding20">
        <label @click="isDictEmpty(selected_day)" class="mini-container">
            <span class="selectRank text">W ten dzień chcę mieć zajęcia</span>
            <input type="checkbox" checked="checked" value=!availability[selected_day][0].available v-model="availability[selected_day][0].available">
            <span class="checkmark"></span>
        </label>
    </div>

    <div v-if="availability[selected_day][0].available" class="selectSchedule rule-wrapper">
        <div v-for="(schedule, index) in availability[selected_day][0].schedule" :key="index">
            od <input type="number" min="0" max="24" v-model="schedule.start" placeholder="wpisz godzinę" class="selectSchedule inputNumber"/>:00
            &nbsp; &nbsp; do <input type="number" min="0" max="24" v-model="schedule.end" placeholder="wpisz godzinę" class="selectSchedule inputNumber"/>:00
            <br>
        </div>
    </div>
    
    <a v-if="availability[selected_day][0].available" @click="addSchedule(selected_day)" class="opacity55"> dodaj</a>
    <a v-if="availability[selected_day][0].available" @click="deleteSchedule(selected_day)" class="opacity55">usuń </a>

    <br><br>

    <button @click="submit" class="submit">Zapisz</button>

</div>
</template>

<script>
import StrikeItem from '@/components/Strike-Item.vue'
import utils from '../../scripts/utils'
import getData from '../../scripts/getData'

export default {
    props: ['subject'],
    components: {
        StrikeItem
    },
    data () {
        return {
            days: ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"],
            selected_day: "Pn",
            selected_day_index: 0,
            availability: {
                Cz: [{name: "czwartek", available: true, schedule: [{start: 11, end: 16}]}],
                Nd: [{name: "niedziela", available: false, schedule: []}],
                Pn: [{name: "poniedziałek", available: true, schedule: [{start: 11, end: 16}]}],
                Pt: [{name: "piątek", available: true, schedule: [{start: 11, end: 16}, {start: 17, end: 19}]}],
                Sb: [{name: "sobota", available: true, schedule: [{start: 8, end: 16}]}],
                Wt: [{name: "wtorek", available: true, schedule: [{start: 11, end: 16}]}],
                Śr: [{name: "środa", available: true, schedule: [{start: 11, end: 16}]}]
            },
        }
    },
    mounted: function () {
        this.$store.commit('set', this.$route.query.rank)
    },
    methods: {
        changeClass(index) {
            if(index == this.selected_day_index){
                return 'selectedDay yes'
            }
            else {
                return 'SelectedDay'
            }
        },
        dayBack(){
            if(this.selected_day_index == 0){
                return
            }
            let new_index = this.selected_day_index - 1
            let new_day = this.days[new_index]
            this.selectDay(new_day, new_index)
        },
        dayUp(){
            if(this.selected_day_index == 6){
                return
            }
            let new_index = this.selected_day_index+1
            let new_day = this.days[new_index]
            this.selectDay(new_day, new_index)
        },
        selectDay (day, index){
            this.selected_day = day
            this.selected_day_index = index
        },
        isDictEmpty(selected_day){
            if(Object.keys(this.availability[selected_day][0].schedule).length == 0){
            this.availability = utils.pushToschedule(this.availability, selected_day)
            }
            if (this.availability[selected_day][0].available){
            this.availability[selected_day][0].schedule = []
            }
        },
        addSchedule(selected_day){
            this.availability[selected_day][0].available = true
            utils.pushToschedule(this.availability, selected_day)
        },
        deleteSchedule(selected_day){
            if(Object.keys(this.availability[selected_day][0].schedule).length == 1){
                this.availability[selected_day][0].available = false
            }
            this.availability[selected_day][0].schedule.pop()
        },
        submit(){
            // tutor_id backend ma z tokenu auth więc nie podaje :)

            fetch(getData.url()+"/create_class/tutor", {
                method: "POST",
                dataType: "json",
                body: JSON.stringify({
                    subject: this.subject,
                    rank: this.$store.state.select_rank.data,
                    availability: this.availability
            }),
                headers: getData.getHeaders(),
            })
            .then(response => {
                if(response.status == 500){
                    alert('error: błąd połączenia z bazą danych... \nkod błędu: 500')
                }
                if(response.status == 418){
                    alert('error: Brak wsparcia dla leniów \nkod błędu: 418')
                }
                if(response.status == 409){
                    alert('Te zajęcia do tego przedmiotu są już stworzone, poinformujemy cię gdy znajdzie się chętny uczeń')
                }
                this.$router.push({ name: 'Dashboard', query: { created: 'success' } })
            })
            .catch(error => {
                alert('Error:', error);
            })
        }
    },
}
</script>

<style>
.selectSchedule.mini-wrapper{
    margin-top: 5px;
    width: 350px;
    height: 60px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}
.selectedDay.yes{
    background-color: #1c2429;
    color: #ccc;
    height: 19px;
    width: 19px;
}
.selectSchedule.day{
    font-weight: 500;
    float: left;
    padding: 10px;
    border-radius: 50%;
    margin: 5px;
    cursor: pointer;
    height: 19px;
    width: 19px;
}

.selectSchedule.arrow{
    float: left;
    height: 40px;
}
.selectSchedule.currentDay{
    padding: 20px;
    font-size: 30px;
    width: 160px;
    text-align: center;
    float: left;
    transform: translateY(-18px);
}
.selectSchedule.currentDay-wrapper{
    margin-left: auto;
    margin-right: auto;
    width: 200px;
    height: 20px;
    float: left;
}
.selectSchedule.mini-wrapper-two{
    height: 70px;
    width: 280px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}
.selectSchedule.inputNumber{
    width : auto;
    font-size: large;
    text-align: center;
    margin-bottom: 15px;
}
.selectSchedule.rule-wrapper{
    font-size: medium;
}
@media only screen and (max-width: 440px) {
    .wrapper.selectSchedule {
      margin-bottom: 100px;
    }
}
</style>