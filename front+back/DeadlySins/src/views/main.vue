<template>
    <div class="background">
        <div class ="header">

        </div>

      <div class="section1">
        <div class="row" style="padding-left:10px">
          <vs-button text-color="rgb(255, 255, 255)" type="flat" icon="menu" to="/analysis">analysis</vs-button>
        </div>
        <div class="row" style="padding-left:10px">
          <vs-button text-color="rgb(255, 255, 255)" type="flat" icon="public" to="/map1">map</vs-button>
        </div>
        <div class="row" style="padding-left:10px">
          <vs-button text-color="rgb(255, 255, 255)" type="flat" icon="person_add" to="/person">author</vs-button>
        </div>
      </div>

      <div class="main">
        <p class="font">We harvest tweets from users in Australia, analyse their text,
        use machine learning techniques (eg: negative words people used; time users usually
        send twitters; the location they used to go; their favourite restaurants .etc)
         to give everyone a score of sloth, and compare them
        with the official data from Aurin. The comparison is based on the median age, median
        weekly personal income and population of each area.  In addtion, we measure the relation
         between number of sex workers and sex crime rate in each area. Click the analysis and
          map button on the top-left to find more.
        </p>
      </div>



    </div>
</template>

<script>

</script>

<style>
.background{
background-color:#06010C;
}
.header{
height:35px;
background-image: url("../assets/images/7S_Skulls.jpg");
background-size: 15%, 100%;
}
.section1{
background-image: url("../assets/images/7-deadly.jpg");
background-size: 80% 100%;
background-repeat: no-repeat;
background-position: center;
height:700px;
}
.main{
padding-left:140px;
height: 400px;
padding-top:100px;
padding-right:140px;
}
.font{
font-size:23px;
color: white;
overflow: auto;
}
</style>
