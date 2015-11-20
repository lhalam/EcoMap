app.controller('MainCtrl', ['$scope', '$http','$auth', '$cookies', function($scope, $http, $auth, $cookies){
  
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

  $http({
    method: 'GET',
    url: '/api/getTitles'
  }).success(function(resp){
    $scope.faqTitles = resp;
    console.log(resp);
  });

}]);
