// app.controller('UserDeleting', ['$scope', '$cookies', '$http', 'toaster',
// function($scope, $cookies, $http, toaster){
// 	$scope.user = {};
//     $scope.user.id = $cookies.get("id");

//      if ($scope.user.id) {
//       $http({
//         url: '/api/user_detailed_info/' + $scope.user.id,
//         method: 'GET'
//       }).success(function(response) {
//         $scope.user.data = response;
//   });
    

//     $scope.printId = function () {
//     	console.log($scope.user.id);
//     	return $scope.user.id;
//     };
    	
// }
// ]);