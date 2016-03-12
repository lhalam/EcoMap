app.controller('MainCtrl', ['$scope', '$http', '$auth', '$rootScope', '$cookies', '$state', 'MapFactory', '$timeout', function($scope, $http, $auth, $rootScope, $cookies, $state, MapFactory, $timeout) {
    $rootScope.isFetching=false;

    $scope.isAuthenticated = function() {
      var authenticated;
      if (!$cookies.get('id')) {
        authenticated =  false;
      }
      else {
        authenticated = $auth.isAuthenticated();
      }
      return authenticated;
    };
    
    $scope.isAdmin = function() {
      var role = $cookies.get('role');
      if (role == 'admin') {
        return true;
      } else {
        return false;
      }
    };
    $scope.checkState = function(state) {
      return $state.is(state);
    };
    $http({
      method: 'GET',
      url: '/api/getTitles'
    }).success(function(resp) {
      $scope.faqTitles = resp;
    });
    console.log($auth.isAuthenticated());
    
    if ($cookies.get("id")) {
      $http({
        method: 'GET',
        url: '/api/user_detailed_info/' + $cookies.get("id")
      }).success(function(responce) {
        $rootScope.UserCredentials = responce.name + ' ' + responce.surname;
      });
    }  
  }
]);