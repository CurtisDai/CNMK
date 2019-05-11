<template>
    <div class="background">
        <div class ="header">
          <vs-button color="dark" icon="menu" to="/dashboard"></vs-button>
          <vs-button color="dark" icon="public" to="/map1" style="float:right"></vs-button>          
        </div>
        <div class="container" style="height:500px; text-align:center">
            <p class="font1">Author<p>
            <p class="font2">Xiaoshu Chen</p>
            <p class="font2">Tengsheng Ho</p>
            <p class="font2">Zhaoqian Dai</p>
            <p class="font2">Leungsuwan Nathaphol</p>
        </div>

    </div>
</template>
<script>
</script>
<style>
.header{
height:40px;
background-image: url("../assets/images/7S_Skulls.jpg");
background-size: 15%, 100%;
}
.background{
background-color:#06010C;
background-repeat: no-repeat;
background-position: center;
background-size: cover;
}
.font1{
font-size:50px;
color: white
}
.font2{
font-size:35px;
color: white
}
</style>
