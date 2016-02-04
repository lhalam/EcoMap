app.controller('UserCtrl', ['$scope', '$http', 'toaster', '$rootScope', 'msg',
  function($scope, $http, toaster, $rootScope, msg) {
    $scope.loadPagination = function() {

      $scope.msg = msg
      $scope.fromPage = 1;
      $scope.bigCurrentPage = 1;
      $scope.UsersLength = $scope.selectCount['selected'];
      $scope.bigTotalItems = $scope.UsersLength / $scope.selectCount['selected'] * 10;
      $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
        var stepCount = $scope.selectCount['selected']
        $http({
          method: 'GET',
          url: '/api/user_page',
          params: {
            per_page: $scope.selectCount['selected'],
            offset: $scope.selectCount['selected'] * newValue - stepCount,
          }
        }).then(function successCallback(data) {
          var UsersObj = data.data[0];
          $scope.UsersLength = data.data[1][0]['total_users'];
          $scope.selectedUsers = UsersObj
          $scope.bigTotalItems = $scope.UsersLength / $scope.selectCount['selected'] * 10;
        }, function errorCallback(response) {
          $scope.msg.editError('користувача');
        })
      });
      $scope.change = function(currPage) {
        $scope.bigCurrentPage = currPage
      }
    }

    $scope.loadPagination();

    $scope.changeRole = function(user_obj) {
      var role_id;
      for (role in $scope.Roles) {
        if (user_obj.role_name === role) {
          role_id = $scope.Roles[user_obj.role_name]
        }
      }
      $http({
        method: 'POST',
        url: '/api/user_roles',
        data: {
          'role_id': role_id,
          'user_id': user_obj.id
        }
      }).then(function successCallback(data) {
        $scope.msg.editSuccess('користувача');
      }, function errorCallback(response) {
        $scope.msg.editError('користувача');
      })
    }
  }
  ])
