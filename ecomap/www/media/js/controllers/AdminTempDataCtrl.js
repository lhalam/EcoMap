app.controller('TempDataCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster,  msg, msgError) {

    $scope.msg = msg;
    $scope.msgError = msgError;
    $scope.loadTempData();

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
