<template>
<h1>Wybierz stopień nauki</h1>

<!-- {{ $store.state.count }} -->

<div class="wrapper selectRank">
    <div class="selectRank miniWrapper">
        <label class="mini-container">
            <span class="selectRank text">początkujący</span>
            <input type="checkbox" checked="checked" value="początkujący" v-model="rank">
            <span class="checkmark"></span>
        </label>
        <label class="mini-container">
            <span class="selectRank text">podstawowy</span>
            <input type="checkbox" value="podstawowy" v-model="rank">
            <span class="checkmark"></span>
        </label>
        <label class="mini-container">
            <span class="selectRank text">średni</span>
            <input type="checkbox" value="średni" v-model="rank">
            <span class="checkmark"></span>
        </label>
        <label class="mini-container">
            <span class="selectRank text">zaawansowany</span>
            <input type="checkbox" value="zaawansowany" v-model="rank">
            <span class="checkmark"></span>
        </label>

        <br><br>
        <button @click="submit" class="submit">Dalej</button>
    </div>
</div>
</template>

<script>
import utils from '../../scripts/utils.js'

export default {
    props: ['subject'],
    data () {
        return {
            rank: []
        }
    },
    mounted: function () {
        if(this.$store.state.select_rank.data == undefined){
            this.rank = ["początkujący"]
        } else {
            let array = utils.encodeRank(this.$store.state.select_rank.data).split(', ')
            array.forEach(element => {
                this.rank.push(element)
            })
        }
    },
    methods: {
        submit(){
            let coded_rank = utils.codeRank(this.rank)
            this.$store.commit('set', coded_rank)
            this.$router.push({ name: 'NewClass-schedule', params: { subject: this.subject}, query: { rank: coded_rank } })
        },
    }
}
</script>

<style>
.selectRank{
    text-align: center;
}
.selectRank.miniWrapper{
    margin-left: auto;
    margin-right: auto;
    width: 165px;
    padding: 25px;
}
.mini-container {
    display: block;
    position: relative;
    margin-bottom: 22px;
    cursor: pointer;
    text-align: left;
  }
  
  /* Hide the browser's default checkbox */
  .mini-container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }
  
  /* Create a custom checkbox */
  .checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 25px;
    width: 25px;
    background-color: #eee;
  }
  
  /* On mouse-over, add a grey background color */
  .mini-container:hover input ~ .checkmark {
    background-color: #ccc;
  }
  
  /* When the checkbox is checked, add a blue background */
  .mini-container input:checked ~ .checkmark {
    background-color: #2196F3;
  }
  
  /* Create the checkmark/indicator (hidden when not checked) */
  .checkmark:after {
    content: "";
    position: absolute;
    display: none;
  }
  
  /* Show the checkmark when checked */
  .mini-container input:checked ~ .checkmark:after {
    display: block;
  }
  
  /* Style the checkmark/indicator */
  .mini-container .checkmark:after {
    left: 9px;
    top: 5px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
    transform: rotate(45deg);
  }
.selectRank.text{
    margin-left: 35px;
    font-size: larger;
}
</style>