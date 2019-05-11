<template>
    <div class="background">
        <div class ="header">
          <vs-button color="dark" icon="public" to="/map1"></vs-button>
          <vs-button color="dark" type="filled" icon="person_add" style="float:right" to="/person"></vs-button>
        </div>

        <!--Charts-->
        <div class="container-fluid mt--7" style="padding-top:95px">
            <div class="row">
                <div class="col-xl-12">
                    <card type="default" header-classes="bg-transparent">
                        <div slot="header" class="row align-items-center">
                            <div class="col">
                                <h5 class="h3 text-white mb-0">Laziness</h5>
                            </div>
                            <div class="col">
                                <ul class="nav nav-pills justify-content-end">

                                </ul>
                            </div>
                        </div>
                        <line-chart
                                :height="350"
                                ref="bigChart"
                                :chart-data="bigLineChart.chartData"
                                :extra-options="bigLineChart.extraOptions"
                        >
                        </line-chart>

                    </card>
                </div>
                </div>

                <div class="row" style="padding-top:30px">
                <div class="col-xl-12">
                    <card header-classes="bg-transparent">
                        <div slot="header" class="row align-items-center">
                            <div class="col">
                                <h5 class="h3 mb-0">Total orders</h5>
                            </div>
                        </div>

                        <bar-chart
                                :height="350"
                                ref="barChart"
                                :chart-data="redBarChart.chartData"
                        >
                        </bar-chart>
                    </card>
                </div>
            </div>
            <!-- End charts-->

            <!--Tables-->
            <div class="row mt-5">
                <div class="col-xl-8 mb-5 mb-xl-0">
                    <page-visits-table></page-visits-table>
                </div>
                <div class="col-xl-4">
                    <social-traffic-table></social-traffic-table>
                </div>
            </div>
            <!--End tables-->
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
        people: '',
        bigLineChart: {
          allData: [
            [0, 20, 10, 30, 15, 40, 20],
            [0, 20, 5, 25, 10, 30, 15]
          ],
          activeIndex: 0,
          chartData: {
            datasets: [],
            labels: [],
          },
          extraOptions: chartConfigs.blueChartOptions,
        },
        redBarChart: {
          chartData: {
            labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'Sales',
              data: [25, 20, 30, 22, 17, 29]
            }]
          }
        }
      };
    },
    created() {
      this.load();

    },
    methods: {
    load() {
      this.axios.get(process.env.STAGE+'json0')
        .then((response) => {
          this.people = response.data;
          for(var a = 0; a < this.people.length; a++) {
            this.label[a] = this.people[a].id;
            this.data1[a] = this.people[a].count
          }
          let chartData = {
            datasets: [
              {
                label: 'Performance',
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
</style>
