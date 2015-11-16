app.controller('UserManagementCtrl', ['$scope',  '$cookies', '$http', '$location', function($scope, $cookies, $http, $location){



   

  $scope.checkLogined = function(){
    if($cookies.get('name') && $cookies.get('surname')){
      return $cookies.get('name') + " " + $cookies.get('surname');
    } else{
      return null;
    }
  }

  

  



}]);
