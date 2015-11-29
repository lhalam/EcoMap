app.controller('addProblemCtrl', ['$scope', '$state', '$http', 'toaster', '$timeout', function($scope, $state, $http, toaster, $timeout) {

    $scope.mapParams = { center: { latitude: 49, longitude: 30 }, zoom: 6 };
    $scope.getMapParams = function(){
        return $scope.mapParams;
    };

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
  $scope.problemTypes =
      [
          {id:'1', name:'option a'},
          {id:'2', name:'type 2'},
          {id:'3', name:'option b'},
          {id:'4', name:'option b'},
          {id:'5', name:'option b'},
          {id:'6', name:'option b'}
      ];

  $scope.newProblem = {
    "title": "",
    "problem_type_id": "",
    "latitude": '49.847743',
    "longtitude": '24.037703'

  };
  $scope.addProblem = function(newProblem, form) {
    $scope.submitted = true;

    if(form.$invalid){
      return;
    }

    $http({
      method: 'POST',
      url: '/api/problem_post',
      data: newProblem
    }).then(function successCallback(response) {
      toaster.pop('success', 'Оповіщення', 'Проблему було успішно додано!');
      $state.go('map');
    }, function errorCallback() {
      toaster.pop('error', 'Помилка при додаванні', 'При спробі додавання проблеми виникла помилка!');
    })
  };


}]);
