app.controller('RegisterCtrl', ['$scope','$http','$cookies', function($scope, $http, $cookies){
  $scope.showRegisterModal = false;
  $scope.toggleRegisterModal = function(){
    $scope.showRegisterModal = !$scope.showRegisterModal;
  }; 

  $scope.newUser = {};
  $scope.Register = function(){
    if(!$scope.newUser.email || !$scope.newUser.firstName ||
      !$scope.newUser.lastName || !$scope.newUser.password ||
      !$scope.newUser.pass_confirm){
      return null;
    }
    if($scope.newUser.password == $scope.newUser.pass_confirm){
      $http({
        method: 'POST',
        url: '/api/register',
        data: $scope.newUser
      }).then(function successCallback(responce){
        $scope.showRegisterModal = false;
        console.log(responce.data);
        $scope.user.email = $scope.newUser.email;
        $scope.user.password = $scope.newUser.password;
        // $scope.Login();
        $scope.newUser = {};
      },
        function errorCallback(responce){});
    }
  };
}]);