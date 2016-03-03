app.controller('MainCtrl', ['$scope', '$http', '$auth', '$rootScope', '$cookies', '$state', 'MapFactory', '$timeout', function($scope, $http, $auth, $rootScope, $cookies, $state, MapFactory, $timeout) {
    $rootScope.isFetching=false;

    $rootScope.showMe = false;
    $rootScope.toogleFilter = function(){
      $rootScope.showMe = !$rootScope.showMe;
      MapFactory.turnResizeOn();
      MapFactory.mapInstance.setZoom(7);
    }
    $scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
    $scope.getUsername = function() {
      if ($cookies.get('name') && $cookies.get('surname')) {
        return $cookies.get('name') + ' ' + $cookies.get('surname');
      } else {
        return null;
      }
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
  }
]);
