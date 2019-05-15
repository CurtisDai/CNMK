<template>
    <div class="background">
        <div class ="header">
          <vs-button color="dark" icon="public" to="/map1"></vs-button>
          <vs-button color="dark" type="filled" icon="person_add" style="float:right" to="/person"></vs-button>
        </div>

        <!--Charts-->
        <div class="container-fluid mt--7" style="padding-top:130px;padding-bottom:35px; height:100%">
            <div class="row">
                <div class="col-xl-12">
                    <card type="default" header-classes="bg-transparent">
                        <div slot="header" class="row align-items-center">
                            <div class="col">
                                <h5 class="h3 text-white mb-0">Income with sloth</h5>
                            </div>
                            <div class="col">
                                <ul class="nav nav-pills justify-content-end">

                                </ul>
                            </div>
                        </div>
                        <line-chart
                                :height="500"
                                ref="bigChart"
                                :chart-data="bigLineChart.chartData"
                                :extra-options="bigLineChart.extraOptions"
                        >
                        </line-chart>

                    </card>
                </div>

                </div>




        </div>

    </div>
</template>
<script>
  // Charts
  import * as chartConfigs from '@/components/Charts/config';
  import LineChart from '@/components/Charts/LineChart';
  import BarChart from '@/components/Charts/BarChart';

  // Tables
  import SocialTrafficTable from './Dashboard/SocialTrafficTable';
  import PageVisitsTable from './Dashboard/PageVisitsTable';

  export default {
    components: {
      LineChart,
      BarChart,
      PageVisitsTable,
      SocialTrafficTable,
    },
    data() {
      return {
        data1: [],
        label: [],
        records: '',
        bigLineChart: {
          activeIndex: 0,
          chartData: {
            datasets: [],
            labels: [],
          },
          extraOptions: chartConfigs.blueChartOptions
        },
      };
    },
    created() {
      this.load();

    },
    methods: {
    load() {
      this.axios.get('http://'+process.env.STAGE+':443/json3')
        .then((response) => {
          this.records = response.data;
          for(var a = 0; a < this.records.length; a++) {
            this.label[a] = this.records[a].median_tot_prsnl_inc_weekly;
            this.data1[a] = this.records[a].score
          }
          let chartData = {
            datasets: [
              {
                label: 'Score',
                data: this.data1
              }
            ],
            labels: this.label,
          };
          this.bigLineChart.chartData = chartData;
          this.bigLineChart.activeIndex = 0;
        })
        setTimeout(this.load, 20000);
        },
    }
  };
</script>
<style>
.header{
height:35px;
background-image: url("../assets/images/7S_Skulls.jpg");
background-size: 15%, 100%;
}
.background{
background-color:#06010C;
background-repeat: no-repeat;
background-position: center;
background-size: cover;
}
</style>
