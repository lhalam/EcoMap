app.factory('MapFactory', ['$window', '$http', '$state', function(win, $http, $state) {
  var instance = {};
  instance.centerMap = {
    lat: 50.468077,
    lng: 30.521018
  };
  instance.zoom = 6;
  instance.initMap = function(centerMap, zoom) {
    if (centerMap === undefined) {
      centerMap = instance.centerMap;
    }
    if (zoom === undefined) {
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
  instance.getInst = function() {
    if (instance.mapInstance) {
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
  instance.loadProblems = function() {
    var markers = [];
    $http({
      method: 'GET',
      url: '/api/problems'
    }).then(function successCallback(response) {
      angular.forEach(response.data, function(marker, key) {
        var pos = {
          lat: marker.latitude,
          lng: marker.longitude
        };
        var new_marker = new google.maps.Marker({
          position: pos,
          map: instance.getInst(),
          id: marker.problem_id,
          problem_type_Id: marker.problem_type_Id,
          problemStatus: marker.status,
          doCluster: true,
          date: marker.date,
          icon: "/image/markers/" + marker.problem_type_Id + ".png",
        });
        new_marker.addListener('click', function() {
          var problem_id = this['id'];
          $state.go("detailedProblem", {
            'id': problem_id
          });
        });
        markers.push(new_marker);
        new_marker.setMap(instance.getInst());
      }, function errorCallback() {})
    })
    return markers;
  }
  instance.setCenter = function(centerMap){
    instance.centerMap = centerMap;
    var map = instance.getInst();

    map.setCenter(centerMap);
  };
  return instance;
}]);