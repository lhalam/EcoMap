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
    $scope.userDeleteConfirmation = function () {
      var data = {};
      data.id = $cookies.get('id');
      console.log("Logout and sent id");
      console.log(data.id);
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
    }
    $scope.userDeleteConfirmation()
    $scope.userDeleteFinal();
    
        

  }]);



// $scope.userDelete = function(){
//       console.log("ENTERED")
//       var data = {}
//       $scope.msg = msg;
//       data.id = $cookies.get('id');
//       console.log(data.id)
//       $http({
//         method: "DELETE",
//         headers: {
//           "Content-Type": "application/json;charset=utf-8"
//         },
//         url: "/api/delete_user_request",
//         data: {
//           'user_id': data.id
//         }
//       }).then(function successCallback(response){
            
//             $scope.msg.sendSuccess('імейлу')
//         }, function errorCallback(){
//             $scope.msg.sendError('імейлу')
//         })
       

// app.controller('DetailedFaqCtrl', ['$scope', '$stateParams', '$state', '$http',
//   function($scope, $stateParams, $state, $http) {
//     $http({
//       url: '/api/resources/' + $stateParams.faqAlias,
//       method: 'GET'
//     }).then(function successCallback(responce) {
//       $scope.faqInfo = responce.data[0];
//     }, function errorCallback() {
//       $state.go('error404');
//     });
//   }
// ]);