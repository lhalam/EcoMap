app.controller('MapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi', function($scope, $http, uiGmapGoogleMapApi) {
  
  $scope.mapReady = true;
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

  uiGmapGoogleMapApi.then(function(maps){
    google.maps.event.trigger(maps, 'resize');
  });

}])