app.controller('UserProfileCtrl', ['$scope', '$rootScope', '$cookies', '$http', function($scope, $rootScope, $cookies, $http){
  $scope.closeProfile = function(){
    $rootScope.userProfile = false;
  };

  $scope.user = {};
  $scope.user.id = $cookies.get("id");

  console.log($scope.user.id);

  $http({
    url: '/api/user_detailed_info/' + $scope.user.id,
    method: 'GET'
  }).success(function(response){
    $scope.user.data = response;
  });

  $scope.selectedTab = "userInfo";
  $scope.setTab = function(tabName){
    $scope.selectedTab = tabName;
  };

  $scope.isSelected = function(tabName){
    return $scope.selectedTab == tabName;
  };
  
}]);