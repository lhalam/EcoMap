app.controller('LoginCtrl', ['$scope','$http','$cookies', '$auth', function($scope, $http, $cookies, $auth){

  $scope.dismiss = function() {
    $scope.$dismiss();
  };

  $scope.invalidPasswordEmail = false;
  $scope.getInvalidPasswordEmail = function(){
    return $scope.invalidPasswordEmail;
  };
  $scope.changeInvalidPasswordEmail = function(){
    $scope.invalidPasswordEmail = false;
  };

  $scope.user = {};

  $scope.Login = function(credentials){
    if(!credentials.email || !credentials.password){
      return null;
    }
    $auth.login(credentials)
      .then(function successCallback(responce){
        $scope.showLoginModal = false;
        $cookies.put('name', responce.data.name);
        $cookies.put('surname', responce.data.surname);
        $cookies.put('id', responce.data.id);

      // $scope.user = {};      
    },
      function errorCallback(responce){
        if(responce.status == 401){
          $scope.invalidPasswordEmail = true;
        } 
      })
    // $http({
    //   method: 'POST',
    //   url: '/api/login',
    //   data: $scope.user
    // }).then(function successCallback(responce){
    //   $scope.showLoginModal = false;
    //   $cookies.put('name', responce.data.name);
    //   $cookies.put('surname', responce.data.surname);
    //   $cookies.put('id', responce.data.id);
    //   $scope.user = {};      
    // },
    //   function errorCallback(responce){
    //     if(responce.status == 401){
    //       $scope.invalidPasswordEmail = true;
    //     } 
    //   });
  };
  
}])
