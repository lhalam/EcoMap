app.controller('LoginCtrl', ['$scope', '$http', '$rootScope','$cookies', '$auth', '$state', 'msg', 'toaster',
  function($scope, $http, $rootScope, $cookies, $auth, $state, msg, toaster) {
    $scope.invalidPasswordEmail = false;
    $scope.msg = msg;
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
        $rootScope.UserCredentials = responce.data.name + ' ' + responce.data.surname ;
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
        $rootScope.UserCredentials = responce.data.name + ' ' + responce.data.surname;
        $state.go('map');
        if (!responce.data.registered) {
          $scope.msg.registerSuccess();
        }
        $rootScope.isFetching=false;
      })
    };
  }
]);

