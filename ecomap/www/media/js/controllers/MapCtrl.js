app.controller('MapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi','$rootScope','uiGmapIsReady',"$state",
  function($scope, $http, uiGmapGoogleMapApi,$rootScope, uiGmapIsReady,$state) {

 if(!$rootScope.mapParams){
   $rootScope.mapParams = {
    center: {
      latitude: 49.357826, 
      longitude: 31.518239
    },
    zoom: 6
  };
 }

  $rootScope.getMapParams = function() {
    return $rootScope.mapParams;
  };

  $rootScope.zoomMarker = function(data) {
    $state.go("detailedProblem",{
      'id':data.model.problem_id
    });
    console.log(data);
    $rootScope.mapParams = {
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
  };

  $scope.loadProblems();

  uiGmapIsReady.promise()
    .then(function(instances) {
      var maps = instances[0].map;
      google.maps.event.trigger(maps, 'resize');
    });
}]);
