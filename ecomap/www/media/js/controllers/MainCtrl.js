app.controller('MainCtrl', ['$scope', '$auth', function($scope, $auth){
  
  $scope.isAuthenticated = function(){
    return $auth.isAuthenticated();
  };

}]);
