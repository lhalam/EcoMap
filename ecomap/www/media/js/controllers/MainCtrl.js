app.controller('MainCtrl', ['$scope', '$http', '$auth', '$rootScope', '$cookies', '$state', 'MapFactory', '$timeout', function($scope, $http, $auth, $rootScope, $cookies, $state, MapFactory, $timeout) {
    $rootScope.isFetching=false;

    $rootScope.metadata = function(){
      metaTags = {
        'title': "Екологічні проблеми України",
        'description': 'Екологічні проблеми України'/*,
        'url': window.location.href,
        'image': ''*/
      }
      return metaTags;
    }

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

    $scope.redirectUserAfterDelete = function() {
      if(!$scope.isAuthenticated()) {
        $state.go('map');
      }
    }
    
    $scope.isAdmin = function() {
      var role = $cookies.get('role');
      if (role == 'admin') {
        return true;
      } else {
        return false;
      }
    };
    
    $scope.isModer = function() {
      var role = $cookies.get('role');
      if (role == 'moderator') {
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
    
    if ($cookies.get("id")) {
      $http({
        method: 'GET',
        url: '/api/user_detailed_info/' + $cookies.get("id")
      }).success(function(responce) {
        $rootScope.Useravatar = responce.avatar;
        $rootScope.UserCredentials = responce.name + ' ' + responce.surname;
      });
    }  
  }
]);