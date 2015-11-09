app.controller('UserProfileCtrl', ['$scope', '$rootScope', '$cookies', '$http', function($scope, $rootScope, $cookies, $http){
  $scope.closeProfile = function(){
    $rootScope.userProfile = false;
  };

  $scope.init = function(){
    var uid = $cookies.get('id');
    $http({
        url: '/api/user_detailed_info/' + uid,
        method: 'GET',
        data: {}
    }).success(function(){

    });
  }
}]);