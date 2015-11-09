app.controller('MainCtrl', ['$scope', '$rootScope', function($scope, $rootScope){
  
  $scope.showUserProfile = function(){
    return $rootScope.userProfile;
  };

}]);