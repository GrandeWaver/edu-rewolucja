<template>
<h1>W jakie dni chcesz mieć zajęcia?</h1>

{{ subject }} {{ $store.state.select_rank.data }}

<div class="wrapper selectSchedule">
    <div v-for="(day, index) in days" :key="index" class="selectSchedule mini-wrapper">
        <div @click="selectDay(day, index)">
            <div class="selectSchedule day" :class="changeClass(index)">{{ day }}</div>
        </div>
    </div>

    <div class="selectSchedule mini-wrapper two">
        <img @click="dayBack" src="@/assets/icons8-back-50.png" class="selectSchedule arrow">
            <div class="selectSchedule currentDay-wrapper">
                <span class="selectSchedule currentDay">{{ selected_day }} </span>
            </div>
        <img @click="dayUp" src="@/assets/icons8-forward-50.png" class="selectSchedule arrow">
    </div>

<!-- 
    <label @click="isDictEmpty(selected_day)" class="mini-container">W ten dzień chcę mieć zajęcia
        <input type="checkbox" checked="checked" value=!availability[selected_day][0].available v-model="availability[selected_day][0].available">
        <span class="checkmark"></span>
    </label> -->
</div>

</template>

<script>
export default {
    props: ['subject'],
    data () {
        return {
            days: ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"],
            selected_day: "Pn",
            selected_day_index: 0,
            // availability: {},
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
        // isDictEmpty(selected_day){
        //     if(Object.keys(this.availability[selected_day][0].schedule).length == 0){
        //     this.availability = this.pushToschedule(this, selected_day)
        //     }
        //     if (this.availability[selected_day][0].available){
        //     this.availability[selected_day][0].schedule = []
        //     }
        // },
    },
    // computed: {
    //      pushToschedule(_this, selected_day){
    //         let last_index = Object.keys(_this.availability[selected_day][0].schedule).length
    //         if(last_index == 0){
    //             _this.availability[selected_day][0].schedule.push(
    //             {
    //                 start: 11,
    //                 end: 16
    //             }
    //             )
    //             return
    //         }
    //         // let last_hour_start = parseInt(_this.availability[selected_day][0].schedule[last_index-1].start)
    //         let last_hour_end = parseInt(_this.availability[selected_day][0].schedule[last_index-1].end)
    //         // walidacja 24 godzin
    //         if(last_hour_end >= 24){
    //             return
    //         }
    //         else{
    //             if(last_hour_end + 3 > 24){
    //             last_hour_end = 24
    //             _this.availability[selected_day][0].schedule.push(
    //                 {
    //                 start: last_hour_end - 1,
    //                 end: last_hour_end
    //                 }
    //             )
    //             }
    //             else{
    //             _this.availability[selected_day][0].schedule.push(
    //                 {
    //                 start: last_hour_end + 1,
    //                 end: last_hour_end + 3
    //                 }
    //             )
    //             }
    //         }
    //         return _this.availability
    //         }
    // }
}
</script>

<style>
.selectSchedule{
    text-align: center;
}
.selectSchedule.mini-wrapper{
    width: 350px;
    margin-left: auto;
    margin-right: auto;
}
.selectedDay{
    font-weight: 500;
}
.selectedDay.yes{
    background-color: #1c2429;
    color: #ccc;
}
.selectSchedule.day{
    float: left;
    padding: 10px;
    border-radius: 50%;
    margin: 5px;
    cursor: pointer;
}
.selectSchedule.arrow{
    float: left;
}
.selectSchedule.currentDay{
    padding: 20px;
    font-size: 44px;
    float: left;
}
.selectSchedule.currentDay-wrapper{
    width: 100px;
    float: left;
}
.selectSchedule.mini-wrapper.two{
    margin-left: auto;
    margin-right: auto;
}

</style>