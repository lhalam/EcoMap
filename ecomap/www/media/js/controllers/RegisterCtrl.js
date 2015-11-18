app.controller('RegisterCtrl', ['$scope','$http','$cookies', '$auth', function($scope, $http, $cookies, $auth){

  $scope.dismiss = function() {
    $scope.$dismiss();
  };

  $scope.newUser = {};
  $scope.Register = function(user){
    if(!user.email || !user.firstName ||
      !user.lastName || !user.password ||
      !user.pass_confirm){
      return null;
    }
    if(user.password == user.pass_confirm){
      $auth.signup(user).then(function successCallback(responce){
        $scope.dismiss();
        var credentials = {};
        credentials.email = $scope.newUser.email;
        credentials.password = $scope.newUser.password;
        $auth.login(credentials).then(function(responce){
          $cookies.put('name', responce.data.name);
          $cookies.put('surname', responce.data.surname);
          $cookies.put('id', responce.data.id);
          $cookies.put('role', responce.data.role);
        });

        $scope.newUser = {};
      },
        function errorCallback(responce){});
    }
  };
}]);