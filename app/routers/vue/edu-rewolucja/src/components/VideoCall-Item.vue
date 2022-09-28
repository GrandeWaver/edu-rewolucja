<template>
<div v-if="!hide" class="videocall wrapper">
    <div @click="hide = true" class="videocall-cancel pointer">X</div>
        <div class="videocall wrapper two">
        <div class="videocall-text">
            Twoja lekcja rozpoczęła się.
            <br>
            <span v-if="$root.userData.account_type == 'student'" class="videocall-text-smaller">
              {{ data.notification.tutor_firstname }} {{ data.notification.tutor_lastname }} za chwilę utworzy spotkanie Zoom.
            </span>
            <span v-if="$root.userData.account_type == 'tutor'" class="videocall-text-smaller">
              Kliknij, aby utworzyć spotkanie z {{ data.notification.student_firstname }} {{ data.notification.student_lastname }}.
            </span>
        </div>
        {{data.notification.status}}
        <span v-if="$root.userData.account_type == 'student'">
            <span v-if="data.notification.status == 'not ready' " class="notAllowed">
              {{data.notification.status}}
              <img src="@/assets/add_to_zoom-unavailable.png" height="32" alt="Dołącz"/>
            </span>
            <span v-else class="pointer">
              <a :href="data.join_url"><img src="@/assets/add_to_zoom.png" height="32" alt="Dołącz"/></a>
            </span>
        </span>
        <span v-if="$root.userData.account_type == 'tutor'" class="pointer">
          <a :href="'https://zoom.us/oauth/authorize?response_type=code&client_id=YsmfYSibRAOiduiok13lPg&redirect_uri=https://app.edu-rewolucja.pl/auth/zoomuser/'+data.lesson_id" target="_blank" rel="noopener noreferrer"><img src="@/assets/add_to_zoom.png" height="32" alt="Dołącz" /></a>
        </span>
    </div>
</div>
</template>

<script>
export default {
    props: ['data'],
    data (){
        return {
          hide: false
        }
    }
}
</script>

<style>
.videocall.wrapper{
    width: 80%;
    height: 250px;
    background-color: #E3E3E3;
    position: relative;
}
.videocall.wrapper.two{
    width: 50%;
    height: 150px;
    margin-top: 50px;
    margin-bottom: 50px;
    background-color: #CECECE;
}
.videocall-text{
    padding: 20px;
    font-size: larger;
}
.videocall-text-smaller{
    font-size: medium;
}
.videocall-cancel{
  position: absolute;
  top: 10px;
  right: 13px;
}

@media only screen and (max-width: 700px) {
  .videocall.wrapper{
    width: 410px;
    }
  .videocall.wrapper.two{
    width: 360px;
  }
}
@media only screen and (max-width: 440px) {
  .videocall.wrapper{
    width: 380px;
}
  .videocall.wrapper.two{
    width: 330px;
}
}
@media only screen and (max-width: 380px) {
  .videocall.wrapper{
    width: 95%;
}
  .videocall.wrapper.two{
    width: 92%;
}
}
</style>