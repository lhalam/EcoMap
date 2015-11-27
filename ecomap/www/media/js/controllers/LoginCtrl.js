app.controller('LoginCtrl', ['$scope', '$http', '$cookies', '$auth', function($scope, $http, $cookies, $auth) {
  $scope.dismiss = function() {
    $scope.$dismiss();
  };

  $scope.invalidPasswordEmail = false;
  $scope.getInvalidPasswordEmail = function() {
    return $scope.invalidPasswordEmail;
  };

  $scope.changeInvalidPasswordEmail = function() {
    $scope.invalidPasswordEmail = false;
  };

  $scope.user = {};
  $scope.Login = function(credentials) {
    $scope.submitted = true;
    if (!credentials.email || !credentials.password) {
      return null;
    }
    $auth.login(credentials).then(function successCallback(responce) {
      $scope.dismiss();
      $cookies.put('name', responce.data.name);
      $cookies.put('surname', responce.data.surname);
      $cookies.put('id', responce.data.id);
      $cookies.put('role', responce.data.role);
    }, function errorCallback(responce) {
      if (responce.status == 401) {
        $scope.invalidPasswordEmail = true;
      }
    });
  };

  $scope.authenticate = function(provider) {
    $auth.authenticate(provider).then(function successCallback(responce) {
      $scope.dismiss();
      $cookies.put('name', responce.data.name);
      $cookies.put('surname', responce.data.surname);
      $cookies.put('id', responce.data.id);
      $cookies.put('role', responce.data.role);
    })
  };

}]);
