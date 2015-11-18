app.controller('MainCtrl', ['$scope', '$auth', '$cookies', function($scope, $auth, $cookies){
  
  $scope.isAuthenticated = function(){
    return $auth.isAuthenticated();
  };

  $scope.getUsername = function(){
    if($cookies.get('name') && $cookies.get('surname')){
      return $cookies.get('name') + " " + $cookies.get('surname');
    } else{
      return null;
    }
  };

  $scope.isAdmin = function(){
    var role = $cookies.get("role");
    if(role == 'admin'){
      return true;
    } else{
      return false;
    }
  };

}]);
