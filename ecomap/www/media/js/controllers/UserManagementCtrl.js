app.controller('UserManagementCtrl', ['$scope',  '$cookies', '$http', '$rootScope', function($scope, $cookies, $http, $rootScope){

  $scope.showLoginModal = false;
  $scope.toggleLoginModal = function(){
    $scope.showLoginModal = !$scope.showLoginModal;
  };

  $scope.showRegisterModal = false;
  $scope.toggleRegisterModal = function(){
    $scope.showRegisterModal = !$scope.showRegisterModal;
  };  

  $scope.checkLogined = function(){
    if($cookies.get('name') && $cookies.get('surname')){
      return $cookies.get('name') + " " + $cookies.get('surname');
    } else{
      return null;
    }
  }

  $rootScope.userProfile = false;
  $scope.triggerUserProfile = function(){
    $rootScope.userProfile = true;
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
        $scope.Login();
        $scope.newUser = {};
      },
        function errorCallback(responce){});
    }
  };

  $scope.invalidPassword = false;
  $scope.getInvalidPassword = function(){
    return $scope.invalidPassword;
  };
  $scope.changeInvalidPassword = function(){
    $scope.invalidPassword = false;
  };

  $scope.user = {};
  $scope.Login = function(){
    if(!$scope.user.email || !$scope.user.password){
      return null;
    }
    $http({
      method: 'POST',
      url: '/api/login',
      data: $scope.user
    }).then(function successCallback(responce){
      $scope.showLoginModal = false;
      $cookies.put('name', responce.data.name);
      $cookies.put('surname', responce.data.surname);
      $cookies.put('id', responce.data.id);
      $scope.user = {};      
      console.log(responce);
    },
      function errorCallback(responce){
        if(responce.status == 401 && responce.data['reason'] == "password"){
          $scope.invalidPassword = true;
        }
      });
  };

  $scope.Logout = function(){
    $http({
      method: 'POST',
      url: '/api/logout',
      data: $scope.user
    }).then(function successCallback(responce){
      $cookies.remove('name');
      $cookies.remove('surname');
      $cookies.remove('id');
    },
      function errorCallback(data){});
  };

}]);
