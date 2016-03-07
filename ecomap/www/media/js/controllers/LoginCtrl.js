app.controller('LoginCtrl', ['$scope', '$http', '$rootScope','$cookies', '$auth', '$state',
  function($scope, $http, $rootScope, $cookies, $auth, $state) {
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
/*        $cookies.put('name', responce.data.name);
        $cookies.put('surname', responce.data.surname);
        $cookies.put('id', responce.data.id);
        $cookies.put('role', responce.data.role);*/
        $state.go('map');
      }, function errorCallback(responce) {
        if (responce.status == 401) {
          $scope.invalidPasswordEmail = true;
        }
      });
    };
    $rootScope.isFetching=false;
    $scope.authenticate = function(provider) {
      $rootScope.isFetching=true;
      setTimeout(function(){
        $rootScope.isFetching=false;
      }, 20000);
      $auth.authenticate(provider).then(function successCallback(responce) {
        // $cookies.put('name', responce.data.name);
        // $cookies.put('surname', responce.data.surname);
        // $cookies.put('id', responce.data.id);
        // $cookies.put('role', responce.data.role);
        $state.go('map');
        $rootScope.isFetching=false;
      })
    };
  }
]);