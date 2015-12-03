app.controller('RegisterCtrl', ['$scope', '$http', '$cookies', '$auth', '$state',
  function($scope, $http, $cookies, $auth, $state) {
    $scope.newUser = {};
    $scope.Register = function(user) {
      $scope.submitted = true;
      if (!user.email || !user.first_name || !user.last_name || !user.password || !user.pass_confirm) {
        return null;
      }
      if (user.password == user.pass_confirm) {
        $auth.signup(user).then(function successCallback(responce) {
          var credentials = {};
          credentials.email = $scope.newUser.email;
          credentials.password = $scope.newUser.password;
          $auth.login(credentials).then(function(responce) {
            $cookies.put('name', responce.data.name);
            $cookies.put('surname', responce.data.surname);
            $cookies.put('id', responce.data.id);
            $cookies.put('role', responce.data.role);
            $state.go('map');
          });
          $scope.newUser = {};
        }, function errorCallback(responce) {});
      }
    };
  }
]);