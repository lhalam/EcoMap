app.controller('MapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi', 'uiGmapIsReady',function($scope, $http, uiGmapGoogleMapApi, uiGmapIsReady) {

  $scope.mapParams = {
    center: {
      latitude: 49,
      longitude: 30
    },
    zoom: 6
  };

  $scope.getMapParams = function() {
    return $scope.mapParams;
  };

  $scope.zoomMarker = function(data) {
    console.log(data);
    $scope.mapParams = {
      center: {
        latitude: data.model.latitude,
        longitude: data.model.longitude
      },
      zoom: 17
    }
  };

  $scope.markers = [];
  $scope.loadProblems = function() {
    $http({
      method: 'GET',
      url: '/api/problems'
    }).then(function successCallback(response) {
      $scope.markers = response.data;
      console.log($scope.markers);
    }, function errorCallback(error) {});
  }

  $scope.loadProblems();
  
  uiGmapIsReady.promise()
    .then(function(instances) {
      var maps = instances[0].map;
      google.maps.event.trigger(maps, 'resize');
    });
}])