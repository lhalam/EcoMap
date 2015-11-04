angular.module('ecomap', ['ui.bootstrap']);

angular.module('ecomap')
  .controller('LoginController', ['$scope', '$http', function($scope, $http){
    $scope.Login = function(){
      $http({
        url: "/api/login",
        method: "POST",
        data: {
          username: $scope.username,
          password: $scope.password
        }
      }).success(function(result){
        console.log(result);
        
      }).error(function(error){
        console.log(error);
      });
    }
  }])
  .controller('LogoutController', ['$scope','$http', function($scope, $http){
    $scope.Logout = function(){
      $http({
        url: "/api/logout",
        method: "POST",
        data: {}
      }).success(function(result){
        console.log(result);
      }).error(function(error){
        console.log(error);
      });
    }
    
  }]);

    var refresh_login = function(val){
      $scope.logined = val;
    }