<template>
<div v-if="show" class="videocall wrapper">
    <div @click="show = false" class="videocall-cancel">X</div>
        <div class="videocall wrapper two">
        <div class="videocall-text">
            Twoja lekcja rozpoczęła się.
            <br>
            Kliknij, aby dołączyć.
        </div>
        <a href="https://zoom.us/oauth/authorize?response_type=code&client_id=YsmfYSibRAOiduiok13lPg&redirect_uri=https://app.edu-rewolucja.pl/auth/zoomuser" target="_blank" rel="noopener noreferrer"><img src="https://marketplacecontent.zoom.us/zoom_marketplace/img/add_to_zoom.png" height="32" alt="Dołącz" /></a>
    </div>
</div>
<!-- {{ data }} -->
</template>

<script>
export default {
    props: ['data'],
    data (){
        return {
            show: true
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