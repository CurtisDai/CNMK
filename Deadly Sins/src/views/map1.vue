<template>
<div class = "background">
    <div class ="header1">
      <vs-button color="dark" icon="menu" to="/dashboard"></vs-button>
      <vs-button color="dark" type="filled" icon="person_add" style="float:right" to="/person"></vs-button>
    </div>

      <div class="col-md-12">
        <div id="map" class="map"></div>
      </div>


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

  }

},

mounted() {
  this.tweetData();
  this.initMap();
},
methods: {

    tweetData() {
    this.axios.get('http://127.0.0.1:5000/json2')
      .then((response) => {
        this.addressPoints = response.data;
      })
      setTimeout(this.load, 20000);
    },
    initMap() {
    this.axios.get('http://127.0.0.1:5000/json1')
      .then((response) => {
        var aurin = response.data;

    var map = L.map('map').setView([-25.2744, 133.7751], 5);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var geo = L.geoJson({features:[]},{onEachFeature:function popUp(f,l){
            var out = [];
            if (f.properties){
                for(var key in f.properties){
                  if (key == 'SA3_CODE16'){

                      for (var au in aurin.features){
                        if (aurin.features[au].properties.sa3_code16==f.properties[key]){
                          out.push("Area_Name"+": "+aurin.features[au].properties.sa3_name16);
                          out.push("median"+ ": "+aurin.features[au].properties.median_tot_hhd_inc_weekly);
                        }
                      }

                  }

                }

            l.bindPopup(out.join("<br />"));
        }
    }}).addTo(map);
    var base = "http://127.0.0.1:5000/SA3_2016_AUST.zip";
    shp(base).then(function(data){
      geo.addData(data);
    });


    var markers = L.markerClusterGroup();
    markers.on('clustermouseover', function (layer) {
      var marks = layer.layer.getAllChildMarkers()
      var sumTitle = 0
      for(var mkr in marks){
      sumTitle+=parseInt(marks[mkr].title )
      }
      layer.sourceTarget
        .bindPopup('<div>'+sumTitle+'</div>', { closeButton: false })
        .openPopup();

    });

    markers.on('clustermouseout', function (layer) {
       layer.sourceTarget.closePopup();
    });

    for (var i = 0; i < this.addressPoints.length; i++) {
      var a = this.addressPoints[i];
      var title = a[2];
      var marker = L.marker(new L.LatLng(a[0], a[1]), {
        title: title
      });
      marker.title = title
      marker.bindPopup(title);
      markers.addLayer(marker);
      marker.on('mouseover', function (e) {
                this.openPopup();
            });
            marker.on('mouseout', function (e) {
                this.closePopup();
            });
    }

    map.addLayer(markers);
  })
    }
},

};
</script>

<style scoped>
.map {
height: 500px;
width: 100%;
}
.background{
background-color:#06010C;
background-repeat: no-repeat;
background-position: center;
background-size: cover;
}
.header1{
height:40px;
background-image: url("../assets/images/7S_Skulls.jpg");
background-size: 15%, 100%;
}
</style>
