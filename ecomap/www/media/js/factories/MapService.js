
app.factory('MapFactory', ['$window', '$http', '$state', function(win, $http, $state) {
  instance = {};
  instance.lat = 49.468077;
  instance.lng = 30.521018;
  instance.centerMap = new google.maps.LatLng(instance.lat, instance.lng);
  instance.zoom = 6;
  instance.markers = [];
  instance.cluster = null;

  instance.initMap = function (centerMap, zoom) {
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
        mapTypeControl: false,
      }
    });
    instance.lat = centerMap.lat;
    instance.lng = centerMap.lng;
    instance.zoom = zoom;
    google.maps.event.addListener(instance.mapInstance, 'dragend', function() {
      instance.centerMap = instance.mapInstance.getCenter();
    });
    google.maps.event.addListener(instance.mapInstance, 'zoom_changed', function() {
      instance.zoom = instance.mapInstance.getZoom();
    });
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
        mapTypeControl: false
      }
    });
  }
  instance.turnResizeOn = function() {
    google.maps.event.addListenerOnce(instance.mapInstance, 'idle', function() {
      google.maps.event.trigger(instance.mapInstance, 'resize');
    });
  }
  instance.loadProblems = function() {
    var markers = [];
    var mcOptions = {gridSize: 80, maxZoom: 13};
    instance.cluster = new MarkerClusterer(instance.getInst(), [], mcOptions);
    $http({
      method: 'GET',
      url: '/api/problems'
    }).then(function successCallback(response) {
      console.log(response);
      angular.forEach(response.data, function (marker, key) {
        if (marker.is_enabled == 0)
          return;
        var pos = new google.maps.LatLng(marker.latitude, marker.longitude);
        var new_marker = new google.maps.Marker({
          position: pos,
          map: instance.getInst(),
          id: marker.problem_id,
          problem_type_Id: marker.problem_type_Id,
          problemStatus: marker.status,
          doCluster: true,
          date: marker.date,
          icon: '/image/markers/' + marker.picture,
          radius: marker.radius
        });
        new_marker.addListener('click', function() {
          var problem_id = this['id'];
          $state.go('detailedProblem', {
            'id': problem_id
          });
        });
        instance.cluster.addMarker(new_marker);
        markers.push(new_marker);
        console.log(instance.cluster.getMaxZoom())
      }, function errorCallback() {})
    })
    instance.markers = markers;
        return instance.markers;
  }
  instance.refreshCluster = function() {
    instance.cluster.clearMarkers();
    angular.forEach(instance.markers, function(marker, key) {
        if (marker.getVisible()) {
          instance.cluster.addMarker(marker);
        }
      });
  };
  instance.setCenter = function(centerMap, zoom) {
    instance.centerMap = centerMap;
    instance.zoom = zoom;
    var map = instance.getInst();
    map.setZoom(instance.zoom);
    map.setCenter(instance.centerMap);
  };
  return instance;
}]);
