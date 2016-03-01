app.controller('RegisterCtrl', ['$scope', '$http', '$cookies', '$rootScope', '$auth', '$state',
  function($scope, $http, $cookies, $rootScope,$auth, $state) {
    $scope.newUser = {};
    $scope.Register = function(user) {
      // $rootScope.isFetching = true;
      $scope.submitted = true;
      if (!user.email || !user.first_name || !user.last_name || !user.nickname || !user.password || !user.pass_confirm) {
        return null;
      }
      if (user.password == user.pass_confirm) {
        $auth.signup(user).then(function successCallback(responce) {
          var credentials = {};
          credentials.email = $scope.newUser.email;
          credentials.password = $scope.newUser.password;
          $auth.login(credentials).then(function(responce) {
            $state.go('map');
            // $rootScope.isFetching = false;
          });
        }, function errorCallback(responce) {
          
        });
      }
    };
  }
]);