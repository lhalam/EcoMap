app.controller("ResourceCtrl", ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster, msg, msgError) {
    $scope.loadPagination = function() {
      $scope.msg = msg
      $scope.fromPage = 1;
      $scope.bigCurrentPage = 1;
      $scope.ResourceLength = $scope.selectCount['selected'];
      $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
        var stepCount = $scope.selectCount['selected']
        $http({
          method: "GET",
          url: "/api/resources",
          params: {
            per_page: $scope.selectCount['selected'],
            offset: $scope.selectCount['selected'] * newValue - stepCount,
          }
        }).then(function successCallback(data) {
          $scope.Resources = data.data[0]
          $scope.ResourceLength = data.data[1][0]['total_res_count']
          $scope.bigTotalItems = $scope.ResourceLength / $scope.selectCount['selected'] * 10;
        }, function errorCallback(response) {
          $scope.msg.editError('користувача');
        })
      });
      $scope.change = function(currPage) {
        $scope.bigCurrentPage = currPage
      }
    }

    $scope.loadPagination();
    $scope.msg = msg
    $scope.msgError = msgError
    $scope.addResModal = false;
    $scope.triggerAddResModal = function() {
      $scope.addResModal = true;
      $scope.newResource = {};
    };
    $scope.editResModal = false;
    $scope.showeditResModal = function(name, id) {
      $scope.editResObj = {
        'name': name,
        'id': id
      };
      $scope.editResModal = true;
    }
    $scope.editResource = function(editResObj) {
      if (!editResObj.name || !editResObj.id) {
        $scope.msg.editError('ресурсу', $scope.msgError['incorectData']);
        return;
      }
      $http({
        method: "PUT",
        url: "/api/resources",
        data: {
          "resource_name": editResObj['name'],
          "resource_id": editResObj['id']
        }
      }).then(function successCallback(data) {
        $scope.loadPagination()
        $scope.editResModal = false;
        $scope.msg.editSuccess('ресурсу');
      }, function errorCallback(response) {
        $scope.msg.editError('ресурсу', $scope.msgError['alreadyExist']);
      })
    };
    $scope.deleteResource = function(id) {
      $http({
        method: "DELETE",
        headers: {
          "Content-Type": "application/json;charset=utf-8"
        },
        url: "/api/resources",
        data: {
          "resource_id": id
        }
      }).then(function successCallback(data) {
        $scope.loadPagination();
        $scope.msg.deleteSuccess('ресурсу');
      }, function errorCallback(response) {
        $scope.msg.deleteError('ресурсу', $scope.msgError['alreadyBinded']);
      })
    };
    $scope.newResource = {};
    $scope.addResource = function(newResource) {
      if (!newResource.name) {
        return;
      }
      $http({
        method: "POST",
        url: "/api/resources",
        data: {
          'resource_name': $scope.newResource.name
        }
      }).then(function successCallback(data) {
        $scope.addResModal = false;
        $scope.Resources[data.data.added_resource] = data.data.resource_id
        $scope.loadPagination();
        $scope.addResModal = false
        $scope.msg.createSuccess('ресурсу');
      }, function errorCallback(response) {
        $scope.addResModal = false;
        $scope.msg.createError('ресурсу', $scope.msgError['alreadyExist']);
      });
    };
}])
