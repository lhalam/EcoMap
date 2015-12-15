app.factory('$map', ['', function() {
    console.log('hello from map service');
  var instance = {};
  instance.centerMap = {
    lat: 49.357826,
    lng: 31.518239
  };
  instance.zoom = 6;

  instance.initMap = function(centerMap, zoom) {
    if(centerMap === undefined){
        centerMap = instance.centerMap;
    }
    if(zoom === undefined){
        zoom = instance.zoom;
    }
    instance.mapInstance = new google.maps.Map(document.getElementById('map'), {
      center: centerMap,
      zoom: zoom,
      options: {
        panControl: true,
        zoomControl: true,
        scaleControl: true,
        mapTypeControl: true,
      }
    });

    instance.centerMap.lat = centerMap.lat;
    instance.centerMap.lng = centerMap.lng;
    instance.zoom = zoom;
  }

  instance.getInst = function(){
    if(instance.mapInstance){
        return instance.mapInstance;
    }

    instance.mapInstance = new google.maps.Map(document.getElementById('map'), {
      center: instance.centerMap,
      zoom: instance.zoom,
      options: {
        panControl: true,
        zoomControl: true,
        scaleControl: true,
        mapTypeControl: true,
      }
    });
  }

  instance.turnResizeOn = function() {
    google.maps.event.addListenerOnce(instance.mapInstance, 'idle', function() {
      console.log("Resizing map...");
      google.maps.event.trigger(instance.mapInstance, 'resize');
    });    
  }

  return {
    init: instance.initMap,
    turnResizeOn: isntance.turnResizeOn,
    getInst: instance.getInst
  };
}])