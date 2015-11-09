app.controller('UserProfileCtrl', ['$scope', '$rootScope', function($scope, $rootScope){
  $scope.closeProfile = function(){
    $rootScope.userProfile = false;
  };
}]);