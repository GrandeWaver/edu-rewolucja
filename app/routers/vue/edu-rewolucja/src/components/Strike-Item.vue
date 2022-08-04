<template>
    <div class="strike"><span>{{ text }}</span></div>
</template>

<script>
export default {
    props: ['text']
}
</script>

<style>
.strike {
    display: block;
    text-align: center;
    overflow: hidden;
    white-space: nowrap; 
    opacity: 0.55;
}

.strike > span {
    position: relative;
    display: inline-block;
}
.strike > span:before,
.strike > span:after {
    content: "";
    position: absolute;
    top: 50%;
    width: 9999px;
    height: 1px;
    opacity: 0.55;
    background: black;
}

.strike > span:before {
    right: 100%;
    margin-right: 15px;
}

.strike > span:after {
    left: 100%;
    margin-left: 15px;
}
</style>