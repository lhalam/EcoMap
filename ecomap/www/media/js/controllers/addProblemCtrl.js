app.controller('addProblemCtrl', ['$scope', '$state', '$http', 'toaster', 'Upload',
    '$timeout', 'uiGmapIsReady',
    function($scope, $state, $http, toaster, Upload, $timeout, uiGmapIsReady) {

    $scope.mapParams = { center: { latitude: 49, longitude: 30 }, zoom: 6 };
    $scope.getMapParams = function(){
        return $scope.mapParams;
    };

    $scope.pattern = {
      'coords': /^[-]{0,1}[0-9]{0,3}[.]{1}[0-9]{0,7}$/
    }

    $scope.zoomMarker = function(data){
        console.log(data);
        $scope.mapParams = {
            center: { latitude: data.model.latitude,
                      longitude: data.model.longitude },
            zoom: 17
        }
    };

    $scope.markers = [];
    $scope.loadProblems = function(){
        $http({
            method: 'GET',
            url: '/api/problems'
        }).then(function successCallback(response){
            $scope.markers = response.data;
            console.log($scope.markers);
        }, function errorCallback(error){});
    };
    $scope.loadProblems();


//FORM for ADDING PROBLEMS
angular.extend($scope, {
        map: {
            center: {
                latitude: 42.3349940452867,
                longitude:-71.0353168884369
            },
            zoom: 11,
            markers: [],
            events: {
            click: function (map, eventName, originalEventArgs) {
                var e = originalEventArgs[0];
                var lat = e.latLng.lat(),lon = e.latLng.lng();
                var marker = {
                    id: Date.now(),
                    coords: {
                        latitude: lat,
                        longitude: lon
                    }
                };
                $scope.map.markers.push(marker);
                console.log($scope.map.markers);
                $scope.$apply();
            }
        }
        }
    });

//var eventsSearchbox = {
//          places_changed: function (searchBox) {}
//        };
//        $scope.searchbox = { template:'searchbox.tpl.html', events:eventsSearchbox};

    $scope.newProblem = {
    "title": "",
    "type": "",
    "latitude": "",
    "longitude": ""
  };

    //$scope.marker = {
    //  id: Date.now(),
    //  coords: {
    //    latitude: $scope.newProblem.latitude || "",
    //    longitude: $scope.newProblem.longitude || ""
    //  },
    //  options: {
    //  draggable: true,
    //  labelContent: 'ваше місцезнаходження',
    //  labelAnchor: "65 0",
    //  labelClass: "marker-labels",
    //  icon:'http://www.sccmod.org/wp-content/uploads/2014/11/mod-map-marker1.png'}
    //}
    $scope.marker = {id: Date.now(),
      coords: {
        //latitude: position.coords.latitude,
        //longitude: position.coords.longitude,
        latitude: $scope.newProblem.latitude,
        longitude: $scope.newProblem.longitude
        //latitude: position.coords.latitude,
        //longitude: position.coords.longitude
      }
    }
  $scope.problemTypes =
      [
        {name: 'Проблеми лісів', id: 1},
        {name: 'Сміттєзвалища', id: 2},
        {name: 'Незаконна забудова', id: 3},
        {name: 'Проблеми водойм', id: 4},
        {name: 'Загрози біорізноманіттю', id: 5},
        {name: 'Браконьєрство', id: 6},
        {name: 'Інші проблеми', id: 7}
      ];

    $scope.createMarker = function(position){
        console.info('created');

    $scope.options = {scrollwheel: false};
    $scope.coordsUpdates = 0;
    $scope.dynamicMoveCtr = 0;

    $scope.marker = {
      id: Date.now(),
      coords: {
        //latitude: position.coords.latitude,
        //longitude: position.coords.longitude,
        latitude: $scope.newProblem.latitude,
        longitude: $scope.newProblem.longitude
        //latitude: position.coords.latitude,
        //longitude: position.coords.longitude
      },
      options: {
      draggable: true,
      labelContent: 'ваше місцезнаходження',
      labelAnchor: "65 0",
      labelClass: "marker-labels",
      icon:'http://www.sccmod.org/wp-content/uploads/2014/11/mod-map-marker1.png'},
      events: {
        dragend: function (marker, eventName, args) {
          console.log('marker dragend');
          var lat = marker.getPosition().lat();
          var lon = marker.getPosition().lng();

        $scope.newProblem.latitude = marker.getPosition().lat();
        $scope.newProblem.longitude =  marker.getPosition().lng();

        $scope.marker.options = {
          draggable: true,
          labelContent: 'location',
          labelAnchor: "20 0",
          labelClass: "marker-labels",
          icon:'https://2ip.com.ua/images/marker_map.png'
          };
        }
      }
    };



    $scope.$watchCollection("marker.coords", function (newVal, oldVal) {
      if (_.isEqual(newVal, oldVal))
        return;
      $scope.coordsUpdates++;
    });
};

$scope.reloadPos = function(){
        //alert('reload');
        //console.log($scope.marker);
        $scope.createMarker();
        $scope.marker.coords.latitude =  $scope.newProblem.latitude;
        $scope.marker.coords.longitude =  $scope.newProblem.longitude;
        $scope.mapParams ={ center: { latitude: $scope.newProblem.latitude,
            longitude: $scope.newProblem.longitude }, zoom: 7 };
    };


var options = {
  enableHighAccuracy: true,
  timeout: 3000,
  maximumAge: 0
};


function error(err) {
  console.warn('ERROR(' + err.code + '): ' + err.message);
}


$scope.locateUser = function() {
    navigator.geolocation.getCurrentPosition(getUserPosition, error, options);
    //navigator.geolocation.getCurrentPosition(success, error, options);
    var width = window.innerWidth;
    function getUserPosition(position) {
        mapCenter = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };
        $scope.newProblem.latitude = position.coords.latitude;
        $scope.newProblem.longitude = position.coords.longitude;
        //var crd = position.coords;
        //  console.log('Your current position is:');
        //  console.log('Latitude : ' + crd.latitude);
        //  console.log('Longitude: ' + crd.longitude);
        //  console.log('More or less ' + crd.accuracy + ' meters.');
        if (width < 1000) {
            $scope.mapParams ={ center: mapCenter, zoom: 10 };
        } else {
            $scope.mapParams ={ center: mapCenter, zoom: 17 };
        }
        $scope.createMarker(position);
     $scope.$apply()
    }

};

  //$scope.addProblem = function(newProblem, form) {
  //  $scope.submitted = true;
  //
  //  if(form.$invalid){
  //    return;
  //  }
  //
  //  $http({
  //    method: 'POST',
  //    url: '/api/problem_post',
  //    headers: {'Content-Type':'multipart/form-data'},
  //    data: {'data': newProblem}
  //  }).then(function successCallback(response) {
  //    toaster.pop('success', 'Оповіщення', 'Проблему було успішно додано!');
  //    $state.go('map');
  //  }, function errorCallback() {
  //    toaster.pop('error', 'Помилка при додаванні', 'При спробі додавання проблеми виникла помилка!');
  //  })
  //};
  $scope.logg = function() {
    $scope.newProblem = {
      'latitude': $scope.latitude,
      'longitude': $scope.longitude
    }
    var width = window.innerWidth;
    // if (width < 1000) {
      $scope.mapParams = {
        center: {
          'longitude': $scope.longitude,
          'latitude': $scope.latitude
        },
        zoom: 15
      }
    // } else {
    //   $scope.mapParams = {
    //     center: {
    //       'longitude': $scope.longitude,
    //       'latitude': $scope.latitude
    //     },
    //     zoom: 15
    //   }
    // }
  }

  $scope.addProblem = function(newProblem, form) {
    $scope.submitted = true;

    if(form.$invalid){
      return;
    }
    console.log(newProblem);
    Upload.upload({
      url: '/api/problem_post',
      method: "POST",
      cache: false,
      headers: {
        'Cache-Control': 'no-cache'
      },
      data: newProblem

      }).then(function successCallback(response) {
      toaster.pop('success', 'Оповіщення', 'Проблему було успішно додано!');
      $state.go('map');
    }, function errorCallback() {
      toaster.pop('error', 'Помилка при додаванні', 'При спробі додавання проблеми виникла помилка!');
    })
  };

    uiGmapIsReady.promise()
    .then(function(instances) {
      var maps = instances[0].map;
      google.maps.event.trigger(maps, 'resize');
    });
}]);
