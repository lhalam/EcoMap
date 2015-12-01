app.controller('MapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi', 'uiGmapIsReady',function($scope, $http, uiGmapGoogleMapApi, uiGmapIsReady) {

  $scope.mapParams = {
    center: {
      latitude: 49.357826, 
      longitude: 31.518239
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
      angular.forEach($scope.markers, function(value, key){
        $scope.markers[key].iconUrl = "/image/markers/" + value.problem_type_Id + ".png";
      });
    }, function errorCallback(error) {});
  }

  $scope.loadProblems();
  
  uiGmapIsReady.promise()
    .then(function(instances) {
      var maps = instances[0].map;
      google.maps.event.trigger(maps, 'resize');
    });
}])