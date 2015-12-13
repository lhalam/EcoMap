app.controller("PermisionCtrl", ['$scope', '$http', 'toaster', 'msg', 
  'msgError', function($scope, $http, toaster, msg, msgError) {
    console.log('$scope.Permision')
    $scope.loadPagination = function() {
      $scope.msg = msg
      $scope.fromPage = 1;
      $scope.bigCurrentPage = 1;

      $scope.permisLength = $scope.selectCount['selected'];
      $scope.$watch('bigCurrentPage', function(newValue, oldValue) {
        console.log($scope.selectCount['selected'])
        var stepCount = $scope.selectCount['selected']
        $http({
          method: "GET",
          url: "/api/all_permissions",
          params: {
            per_page: $scope.selectCount['selected'],
            offset: $scope.selectCount['selected'] * newValue - stepCount,
          }
        }).then(function successCallback(data) {
          $scope.Permision = data.data[0]
          $scope.permisLength = data.data[1][0]['total_perm_count']
          $scope.bigTotalItems = $scope.permisLength / $scope.selectCount['selected'] * 10;
          console.log(data)
        }, function errorCallback(response) {
          $scope.msg.editError('користувача');
        })
      });
      $scope.change = function(currPage) {
        $scope.bigCurrentPage = currPage
      }
    }
    $scope.loadPagination ()
    $scope.addPermModal = false;
    $scope.msgError = msgError;
    $scope.msg = msg;
    $scope.showAddPermModal = function() {
      $scope.addPermModal = true;
      $scope.perm = {};
    };

    $scope.show = function() {
      var name = $scope.perm.resource_name
    }

    $scope.addPermSubmit = function(perm) {
      if (!perm.action || !perm.modifier || !perm.description) {
        return;
      }
      for(res_id in $scope.Resources){
        if($scope.Resources[res_id] === $scope.perm.resource_name){
          var id = res_id;
        }
      }
      $http({
        method: "POST",
        headers: {
          "Content-Type": "application/json;"
        },
        url: "/api/permissions",
        data: {
          "resource_id": id,
          "action": $scope.perm['action'],
          "modifier": $scope.perm['modifier'],
          "description": $scope.perm['description']
        }
      }).then(function successCallback(data) {
        $scope.addPermModal = false;
        $scope.msg.createSuccess('права');
        $scope.loadPagination()
      }, function errorCallback(response) {
        console.log(response)
        $scope.msg.createError('права');
      });
    };

    $scope.editPermModal = false;
    $scope.showEditPermModal = function(perm) {
      $scope.editPerm = perm
      $scope.editPermModal = true;
    }

    $scope.editPermSubmit = function(id) {
      if (!$scope.editPerm.permission_id || !$scope.editPerm['action'] ||
        !$scope.editPerm.modifier || !$scope.editPerm['description']) {
        $scope.msg.editError('права', $scope.msgError['incorectData'])
      return;
    }
    $http({
      method: "PUT",
      url: "/api/permissions",
      data: {
        "permission_id": $scope.editPerm.permission_id,
        "action": $scope.editPerm['action'],
        "modifier": $scope.editPerm.modifier,
        "description": $scope.editPerm['description']
      }
    }).then(function successCallback(data) {
      $scope.editPermModal = false;
      $scope.msg.editSuccess('права');
      $scope.loadPagination()
    }, function errorCallback(response) {
      $scope.msg.editError('права');
    })
  };

  $scope.deletePerm = function(perm) {
    $http({
      'method': "DELETE",
      'headers': {
        "Content-Type": "application/json;charset=utf-8"
      },
      'url': "/api/permissions",
      "data": {
        "permission_id": perm.permission_id
      }
    }).then(function successCallback(data) {
      console.log(data)
      if (!data.data.error) {
        $scope.loadPerm()
        $scope.msg.deleteSuccess('права');
        $scope.loadPagination()

      } else {
        $scope.msg.deleteError('права', $scope.msgError['alreadyBinded']);
      }
    }, function errorCallback(response) {
      $scope.msg.deleteError('права', $scope.msgError['alreadyBinded']);
    })
  }
}]);
