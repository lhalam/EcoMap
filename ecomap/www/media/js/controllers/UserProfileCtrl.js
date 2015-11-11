app.controller('UserProfileCtrl', ['$scope', '$cookies', '$http', function($scope, $cookies, $http){

  $scope.user = {};
  $scope.user.id = $cookies.get("id");

  $scope.body = angular.element(document.body);
  $scope.body.addClass("body-scroll-shown");

  if($scope.user.id){
      $http({
        url: '/api/user_detailed_info/' + $scope.user.id,
        method: 'GET'
      }).success(function(response){
        $scope.user.data = response;
      });
  }

  $scope.selectedTab = "userInfo";
  $scope.setTab = function(tabName){
    $scope.selectedTab = tabName;
  };
  $scope.isSelected = function(tabName){
    return $scope.selectedTab == tabName;
  };

  // $scope.password = {};
  $scope.changePassword = function(){
    var data = {};
    data.id = $cookies.get('id');
    data.old_pass = $scope.password.old_pass;
    data.new_pass = $scope.password.new_pass;
    console.log(data);
    $http({
        method: 'POST',
        url: '/api/change_password',
        data: data
    }).then(function successCallback(responce){
        $scope.changePasswordForm.$setPristine();   //not working???
        $scope.password = {};
        $scope.alert = true;
      // alert pass changed
    },
      function errorCallback(responce){
        if(responce.status == 401){
          $scope.wrongOldPass = true;
        }
      });
  };

  $scope.wrongOldPass = false;
  $scope.getWrongPass = function(){
    return $scope.wrongOldPass;
  };
  $scope.changeWrongPass = function(){
    $scope.wrongOldPass = false;
  };

  $scope.alert = false;
  $scope.closeAlert = function() {
    $scope.alert = false;
  };
  $scope.showAlert = function(){
    return $scope.alert;
  };

  $scope.$on("$destroy", function handler() {
    $scope.body.removeClass("body-scroll-shown");
  });
  
}]);