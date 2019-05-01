<template>
<div>
<div>
  <p>{{ total }}</p>
  <p>{{ status }}</p>
</div>
<div >
  <div class="chart">
    <chartjs-doughnut v-bind:labels="labels"
    v-bind:datasets="datasets"
    v-bind:option="option"></chartjs-doughnut>
  </div>
  <div class="chart">
    <chartjs-line v-bind:labels="labels"
    v-bind:datasets="datasets1"
    v-bind:option="option"></chartjs-line>
  </div>
  <div class="chart">
    <chartjs-bar v-bind:labels="labels1"
    v-bind:datasets="datasets2"
    v-bind:option="option"></chartjs-bar>
  </div>
</div>
<div>
  <p class="text">{{ Count }}</p>
  <p class="text"><span v-for="item in people">{{ item.name+' ' }}</span></p>
</div>
</div>

</template>

<script>
export default{
  data() {
    return {
      timer: '',
      count: '',
      people: '',
      status: '',
      total: 0,
      labels: ["Apples", "Bananas", "Grapes", "Peach"],
      labels1: ["Total"],
      datasets: [
        {
          data: [15,40,50,21],
          backgroundColor: ["Red","Yellow", "Purple","Blue"]
        }
      ],
      datasets1: [
        {
          data: [40,21,16,30],
          backgroundColor: ["grey"],
          label: ["Count"]
        }
      ],
      datasets2: [
        {
          data: [15],
          backgroundColor: ["grey"],
          label: ["Count"]
        }
      ],
      option: {
        title: {
          display: true,
          position: "bottom",
          text: "Fruits"
        }
      },
    }
},
  created() {
    this.load1();
    this.load2();
  },
  methods: {
  load1() {
    this.$http.get('https://restcountries.eu/rest/v1/all')
      .then((response) => {
        this.people = response.data;
      })
      .catch(function(error) {
        console.log(error);
      })
      },
  load2() {
    this.$http.get('http://ron-swanson-quotes.herokuapp.com/v2/quotes')
      .then((response) => {
        this.status = response.data[0];
        this.total += 1;
        })
        .catch(function(error) {
          console.log(error);
        })
      setTimeout(this.load2, 3000);
  }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  computed: {
  Count () {
    return this.people.length
  }
}
};

</script>

<style scoped>
  .chart{
    display: inline-block;
  }
  .text{
    font-size: 8px;
  }
</style>
