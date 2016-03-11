app.controller('TempDataCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster,  msg, msgError) {

    $scope.msg = msg;
    $scope.msgError = msgError;
    
    $scope.loadPagination = function() {
      $scope.msg = msg
      $scope.fromPage = 1;
      $scope.bigCurrentPage = 1;
      $scope.TempdataLength = $scope.selectCount['selected'];
      $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
        var stepCount = $scope.selectCount['selected'];
        $http({
          method: 'GET',
          url: '/api/tempdata',
          params: {
            per_page: $scope.selectCount['selected'],
            offset: $scope.selectCount['selected'] * newValue - stepCount
          }
        }).then(function successCallback(data) {
          $scope.Tempdata = data.data[0];
          $scope.TempdataLength = data.data[1][0]['total_tempdata_count'];
          $scope.bigTotalItems = $scope.TempdataLength / $scope.selectCount['selected'] * 10;
        }, function errorCallback(data) {
          $scope.msg.editError('користувача');
        })
      });
      
    }
    $scope.loadPagination();

    $scope.deleteAllTempData = function(id) {
      $http({
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        url: '/api/tempdata',
      }).then(function successCallback(data) {
        $scope.loadTempData();
        $scope.msg.deleteSuccess('тимчасових даних');
      }), function errorCallback(response) {
        $scope.msg.editError('тимчасових даних', arguments[0]['data']['msg']);
      };
    };


    $scope.deleteTempData = function(id) {
      $http({
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        url: '/api/tempdata',
        data: {
          'user_operation_id': id
        }
      }).then(function successCallback(data) {
        $scope.loadTempData();
        $scope.msg.deleteSuccess('тимчасових даних');
      }), function errorCallback(response) {
        $scope.msg.editError('', arguments[0]['data']['msg']);
      };
    };

  }])

