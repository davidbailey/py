<!doctype html>
<html lang="en">
  <head>
    <style>
      .map {
        height: 100%;
        width: 100%;
      }
    </style>
    <script src="http://openlayers.org/en/v3.9.0/build/ol.js" type="text/javascript"></script>
    <title>speeds.py</title>
  </head>
  <body>
    <div id="map" class="map"></div>
    <script type="text/javascript">
      var stops = {{!stops}};
      var speeds = {{!speeds}};
      var stopSource = new ol.source.Vector({
        features: (new ol.format.GeoJSON()).readFeatures(stops, { featureProjection: 'EPSG:3857' })
      });
      var speedSource = new ol.source.Vector({
        features: (new ol.format.GeoJSON()).readFeatures(speeds, { featureProjection: 'EPSG:3857' })
      });
      var stopStyleFunctionCreator = function() {
	return function(feature, resolution) {
	  var style =  new ol.style.Style({ 
	    text: new ol.style.Text({ text: feature.getId(), scale: 1.5, fill: new ol.style.Fill({ color: 'rgba(0, 0, 0, 1)' }), stroke: new ol.style.Stroke({ color: 'rgba(255, 255, 255, 1)' }), offsetY: 20, offsetX: 20 }), 
	    image: new ol.style.Circle({ radius: 5, fill: new ol.style.Fill({ color: 'rgba(255, 0, 0, 1)' }) }) 
	  }) 
	return [style];
	}
      }
      var speedStyleFunctionCreator = function() {
	return function(feature, resolution) {
	  var style =  new ol.style.Style({ 
	    text: new ol.style.Text({ text: feature.getId(), scale: 1.5, fill: new ol.style.Fill({ color: 'rgba(0, 0, 0, 1)' }), stroke: new ol.style.Stroke({ color: 'rgba(255, 255, 255, 1)' }),  }), 
	  }) 
	return [style];
	}
      }
      var stopLayer = new ol.layer.Vector({
	source: stopSource,
        style: stopStyleFunctionCreator()
      });
      var speedLayer = new ol.layer.Vector({
	source: speedSource,
        style: speedStyleFunctionCreator()
      });
      var tileLayer = new ol.layer.Tile({
        source: new ol.source.OSM()
      });
      var map = new ol.Map({
        target: 'map',
        layers: [tileLayer, stopLayer, speedLayer],
        view: new ol.View({
          center: ol.proj.transform([-98.58, 39.83], 'EPSG:4326', 'EPSG:3857'),
          zoom: 4
        })
      });
    </script>
  </body>
</html>
