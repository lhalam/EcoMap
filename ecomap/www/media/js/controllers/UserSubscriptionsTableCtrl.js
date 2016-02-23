app.controller('UserSubscriptionsTableCtrl', ['$scope', '$state', '$http', '$cookies',
  function($scope, $state, $http, $cookies) {
      $scope.sortType = 'id'; // set the default sort type
      $scope.sortReverse = false;  // set the default sort order
      $scope.searchFish = '';
      $scope.close = function() {
        $state.reload();
      };
      $scope.selectCountObj = {
        '1': '5',
        '2': '10',
        '3': '15',
        '4': '20'
      }
      $scope.selectCount = {
        'selected': '5'
      }

      $scope.getStatus = function(status) {
        var statuses = {
          'Unsolved': 'Не вирішено',
          'Solved': 'Вирішено'
        };
        return statuses[status];
      };
      $scope.showTable = false;
      $scope.loadProblems = function() {
        user_id = $cookies.get('id');
        $scope.msg = msg;
        $scope.fromPage = 1;
        $scope.bigCurrentPage = 1;
        $scope.problemsLength = $scope.selectCount['selected'];
        $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
        $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
          var stepCount = $scope.selectCount['selected']          
          $http({
            method: 'GET',
              url: 'api/usersSubscriptions/' + user_id,
              params: {
                per_page: $scope.selectCount['selected'],
                offset: $scope.selectCount['selected'] * newValue - stepCount,
              }
            }).then(function successCallback(response) {
              $scope.subscriptions = response.data[0];
              $scope.problemsLength = response.data[1][0]['total_problem_count'];
              $scope.bigTotalItems = $scope.problemsLength / $scope.selectCount['selected'] * 10;
            })            
          })
};
$scope.loadProblems();
$scope.detailedInfoModal = false;
$scope.triggerDetailModal = function(problem_id) {
  $scope.detailedInfoModal = !$scope.detailedInfoModal;
  $scope.current_problem_id = problem_id;
  $http({
    method: 'GET',
    url: '/api/problem_detailed_info/' + problem_id
  }).then(function successCallback(response) {
    $scope.detailedProblem = response.data[0][0];
    $scope.comments = response.data[3];
  })
}

  $scope.cls_eye_subs = "fa fa-eye";    
  $scope.chgEyeSubsc = function(){
    if ($scope.cls_eye_subs === "fa fa-eye-slash"){
      $http({
        method: 'POST',
        url: '/api/subscription_post',
        data: {
          'problem_id': $scope.current_problem_id
        }
      }).then(function successCallback(response) {
        $scope.cls_eye_subs = "fa fa-eye";
        $scope.msg.createSuccess('підписки');
      })
      
    }
    else if ($scope.cls_eye_subs = "fa fa-eye") {
      $http({
      method: 'DELETE',
      url: '/api/subscription_delete',
      params: {
        problem_id: $scope.current_problem_id
      }
      }).then(function successCallback(response) {
        $scope.cls_eye_subs = "fa fa-eye-slash";
        $scope.msg.deleteSuccess('підписки');
      })          
    }
};
}
]);