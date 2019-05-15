<template>
<div class = "background">
    <div class ="header1">
      <vs-button color="dark" icon="menu" to="/analysis"></vs-button>
      <vs-button color="dark" type="filled" icon="person_add" style="float:right" to="/person"></vs-button>
    </div>


        <div id="map" class="col-md-12 map"></div>



</div>

</template>

<script>
export default {
data() {
  return {
  aurin: '',
  map: null,
  tileLayer: null,
  addressPoints : [],
  house: [],
  geo1: [],
  geo2: [],
  lga: []
  }

},

mounted() {
  this.lgaData();
  this.geoData1();
  this.geoData2();
  this.tweetData();
  this.houseData();
  this.initMap();
},
methods: {
  lgaData() {
  this.axios.get('http://'+process.env.STAGE+':443/lga')
    .then((response) => {
      this.lga = response.data;
      })
      setTimeout(this.load, 20000);
  },
  geoData1() {
  this.axios.get('http://'+process.env.STAGE+':443/geo1')
    .then((response) => {
      this.geo1 = response.data;
  })
  setTimeout(this.load, 20000);
  },
  geoData2() {
  this.axios.get('http://'+process.env.STAGE+':443/geo2')
    .then((response) => {
      this.geo2 = response.data;
  })
  setTimeout(this.load, 20000);
  },
    tweetData() {
    this.axios.get('http://'+process.env.STAGE+':443/json2')
      .then((response) => {
        this.addressPoints = response.data;
      })
      setTimeout(this.load, 20000);
    },
    houseData() {
    this.axios.get('http://'+process.env.STAGE+':443/json4')
      .then((response) => {
        this.house = response.data;
      })
      setTimeout(this.load, 20000);
    },
    initMap() {
    this.axios.get('http://'+process.env.STAGE+':443/json1')
      .then((response) => {
        var aurin = response.data;

    var map = L.map('map').setView([-25.2744, 133.7751], 5);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var geo1 = L.geoJson(this.geo1,{onEachFeature:function popUp(f,l){
            var out = [];
            if (f.properties){
                      for (var au in aurin.features){
                        if (aurin.features[au].properties.sa3_name16==f.properties.SA3_NAME16){
                          out.push("Area Name"+": "+aurin.features[au].properties.sa3_name16);
                          out.push("Average Population"+ ": "+aurin.features[au].properties.population);
                          out.push("Average Household Size"+": "+aurin.features[au].properties.average_household_size);
                          out.push("Median Age"+": "+aurin.features[au].properties.median_age_persons);
                          out.push("Median Monthly Mortgage Repay"+": "+aurin.features[au].properties.median_mortgage_repay_monthly);
                          out.push("Median Weekly Rent"+": "+aurin.features[au].properties.median_rent_weekly);
                          out.push("Median Weekly Family Income"+ ": "+aurin.features[au].properties.median_tot_fam_inc_weekly);
                          out.push("Median Weekly Household Income"+ ": "+aurin.features[au].properties.median_tot_hhd_inc_weekly);
                          out.push("Median Weekly Personal Income"+ ": "+aurin.features[au].properties.median_tot_prsnl_inc_weekly);
                  }
                }
            l.bindPopup(out.join("<br />"));
        }
    }});

    var lga1 = this.lga

    var geo2 = L.geoJson(this.geo2,{onEachFeature:function popUp(f,l){
        var out = [];
        if (f.properties){
              for (var n in lga1){
                if (lga1[n].lga_code==f.properties.LGA_CODE16){
                  l.setStyle({fillColor: '#E04D11'});
                  out.push("Sexual offences"+": "+lga1[n].all_sexual_offences);
                }
              }
        l.bindPopup(out.join("<br />"));
        }
    }});

    var Layer1 = {
			"SA3": geo1,
      "LGA": geo2
		};

    L.control.layers(Layer1).addTo(map);

    var markers = L.markerClusterGroup();
    markers.on('clustermouseover', function (layer) {
      var marks = layer.layer.getAllChildMarkers()
      var sumTitle = 0
      var sum = 0
      for(var mkr in marks){
        var str = marks[mkr].title.split(" ");
        sumTitle+=parseInt(str[0])
        sum += parseInt(str[1])
      }
      layer.sourceTarget
        .bindPopup('<div>'+sumTitle+' people '+sum+' prostitutes'+'</div>', { closeButton: false })
        .openPopup();
    });

    markers.on('clustermouseout', function (layer) {
       layer.sourceTarget.closePopup();
    });

    for (var i = 0; i < this.addressPoints.length; i++) {
          var a = this.addressPoints[i];
          var title = a['number'].toString();
          var lust = a['lust'].toString();
          var marker = L.marker(new L.LatLng(a['y'], a['x']), {
            title: title
          });
          marker.title = title + " " + lust
          markers.addLayer(marker);
         }
        map.addLayer(markers);

     var Icon = L.icon({
        iconUrl: "http://"+process.env.STAGE+":443/image",
        iconSize: [12, 12],
    });

    for (var i = 0; i < this.house.length; i++) {
      var a = this.house[i];
      var title1 = a['Name'];
      var houseMarker = L.marker(new L.LatLng(a['lat'], a['lon']), {
        title: title1,
        icon: Icon
      });
      houseMarker.title = title
      houseMarker.bindPopup(title1);
      houseMarker.bindPopup(title1);
      houseMarker.on('mouseover', function (e) {
                this.openPopup();
            });
      houseMarker.on('mouseout', function (e) {
                this.closePopup();
            });
      houseMarker.addTo(map)
    }

  })
    }
},

};
</script>

<style scoped>
.map {
height: 100%;
width: 100%;
}
.background{
background-color:#06010C;
background-repeat: no-repeat;
background-position: center;
background-size: cover;
height:800px
}
.header1{
height:35px;
background-image: url("../assets/images/7S_Skulls.jpg");
background-size: 15%, 100%;
}
</style>
