app.controller('userDeleteConfirmation', ['$scope', '$state','$cookies', '$http', 'toaster', '$timeout', '$stateParams', '$auth',
  function($scope, $state, $cookies, $http, toaster, $timeout, $stateParams, $auth) {
    $scope.hashParam = $stateParams.hash_sum
    $scope.user = {}; 
    $scope.user.id = $cookies.get("id");
    $scope.Logout = function() {
      $http({
        method: 'POST',
        url: '/api/logout'
      }).then(function successCallback(responce) {
        $cookies.remove('name');
        $cookies.remove('surname');
        $cookies.remove('id');
        $cookies.remove('role');
        $auth.logout();
        $state.go('map');
      }, function errorCallback(data) {});
    };
    $scope.userDeleteFinal = function(){
      $http({
        method: 'DELETE',
        headers: {
          'Content-Type':'application/json;charset=utf-8'
        },
        url:'/api/user_delete',
        data: {
          'hash_sum' : $scope.hashParam
        }
      });
    };
    $scope.userDeleteConfirmation = function () {
      var data = {};
      data.id = $cookies.get('id');
      $http({
        method: 'GET',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        url : '/api/delete_user_page/' + $scope.hashParam,
        data: {
          'user_id': data.id
        }
      }).then(function successCallback(responce){
        $scope.Logout();
        $scope.userDeleteFinal();
      }, function errorCallback(data) {});
      };
    
    
      $scope.userDeleteConfirmation();      

  }]);