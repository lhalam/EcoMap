app.controller('LogoutCtrl', ['$scope','$http','$cookies','$auth','$state', function($scope, $http, $cookies, $auth, $state){
    $scope.Logout = function(){
    $http({
      method: 'POST',
      url: '/api/logout'
    }).then(function successCallback(responce){
      $cookies.remove('name');
      $cookies.remove('surname');
      $cookies.remove('id');
      $auth.logout();
      $state.go('/map');

      // $scope.newUser = {};
      // $scope.user = {};
      // angular.element(document.querySelector('#loginForm')).$setPristine();
      // angular.element(document.querySelector('#registerForm')).$setPristine();
    },
      function errorCallback(data){});

  };
}])