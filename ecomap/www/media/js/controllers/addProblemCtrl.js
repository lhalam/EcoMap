app.controller('addProblemCtrl', ['$scope', '$state', '$http', 'toaster', 'Upload', '$timeout', function($scope, $state, $http, toaster, Upload, $timeout) {

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
        {name: 'Проблеми лісів', id: 1},
        {name: 'Сміттєзвалища', id: 2},
        {name: 'Незаконна забудова', id: 3},
        {name: 'Проблеми водойм', id: 4},
        {name: 'Загрози біорізноманіттю', id: 5},
        {name: 'Браконьєрство', id: 6},
        {name: 'Інші проблеми', id: 7}
      ];

$scope.locateUser = function() {
            navigator.geolocation.getCurrentPosition(getUserPosition);
            var width = window.innerWidth;
            function getUserPosition(position) {
                var mapCenter = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                if (width < 1000) {
                    $scope.mapParams ={ center: mapCenter, zoom: 15 };
                } else {
                    $scope.mapParams ={ center: mapCenter, zoom: 15 };
                }
            }
        };

  $scope.newProblem = {
    "title": "",
    "type": "",
    "latitude": '49.847743',
    "longitude": '24.037703'

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
  $scope.addProblem = function(newProblem, form) {
    $scope.submitted = true;

    if(form.$invalid){
      return;
    }
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


}]);
