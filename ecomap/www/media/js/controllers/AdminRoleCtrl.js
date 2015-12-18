app.controller("RoleCtrl", ['$scope', '$http', 'toaster', 'msg', 'msgError',
    function($scope, $http, toaster, msg, msgError) {

  $scope.msg = msg;
  $scope.msgError = msgError;
  $scope.addRoleModal = false;
  $scope.showAddRoleModal = function() {
    $scope.addRoleModal = true;
    $scope.role = {};
  }

  $scope.addRoleSubmit = function(role) {
    if (!role.name) {
      return;
    }
    $http({
      method: "POST",
      url: "/api/roles",
      data: {
        "role_name": $scope.role['name']
      }
    }).then(function successCallback(data) {
      $scope.msg.createSuccess('ролі');
      $scope.Roles[data.data.added_role] = data.data.added_role_id;
      $scope.addRoleModal = false;
    }, function errorCallback(response) {
      $scope.msg.createError('ролі', $scope.msgError['alreadyExist']);
    })
  };

  $scope.deleteRole = function(id) {
    $http({
      method: "DELETE",
      headers: {
        "Content-Type": "application/json;charset=utf-8"
      },
      url: "/api/roles",
      data: {
        "role_id": id
      }
    }).then(function successCallback(data) {
      for (r in $scope.Roles) {
        if ($scope.Roles[r] == data.data['deleted_role']) {
          delete $scope.Roles[r];
          $scope.msg.deleteSuccess('ролі');
        }
      }
      if (data.data.error) {
        $scope.msg.deleteError('ролі', $scope.msgError['alreadyBinded']);
      }
    }, function errorCallback(response) {
      $scope.msg.deleteError('ролі', $scope.msgError['alreadyBinded']);
    })
  }

  $scope.editRoleObj = {};
  $scope.editRole = function(role) {
    // if (!$scope.role.name) {
    //   return;
    // }
    $http({
      method: "PUT",
      url: "/api/roles",
      data: {
        "role_name": $scope.editRoleObj['name'],
        "role_id": $scope.editRoleObj['id']
      }
    }).then(function successCallback(data) {
      $scope.loadRole();
      $scope.msg.editSuccess('ролі');
      $scope.rolePermObj.name = $scope.editRoleObj['name'];
      $scope.editRoleModal = false;
    }, function errorCallback(response) {
      $scope.msg.editError('ролі', $scope.msgError['alreadyExist']);
    })
  }

  $scope.editRoleModal = false
  $scope.showEditRoleModal = function(name, id) {
    $scope.editRoleObj = {
      'name': name,
      "id": id
    }
    $scope.editRoleModal = true;
    $scope.listToSend = [];
  }
  $scope.rolePerm = false
  $scope.selectPerm = function(ev, perm) {
    if ($scope.listToSend.indexOf(perm.permission_id) === -1) {
      $scope.listToSend.push(perm.permission_id);
    } else {
      $scope.listToSend.splice($scope.listToSend.indexOf(perm.permission_id), 1)
    }
  }

  $scope.isChecked = function(perm) {
    if ($scope.listToSend) {
      if ($scope.listToSend.indexOf(perm.permission_id) !== -1) {
        return true;
      }
    }
  }

  $scope.backToRole = function() {
    $scope.rolePermTable = true;
    $scope.rolePermBlock = false;
  }
  $scope.editRoleSubFunc =  function () {
    $scope.editRoleSub = true;
  }
  $scope.rolePermTable = true;
  $scope.rolePermBlock = false;
  $scope.showRolePerm = function(name, id) {
    $scope.rolePermTable = false
    $scope.rolePermBlock = true
    $scope.rolePermObj = {
      "name": name,
      "id": id
    }
    $scope.selectPermObj = {}
    $scope.listToSend = []
    $http({
      method: "GET",
      url: "/api/role_permissions",
      params: {
        role_id: $scope.rolePermObj.id
      }
    }).then(function successCallback(data) {
      $scope.actualPermInRole = data.data.actual
      for (var i = 0; i < $scope.actualPermInRole.length; i++) {
        if ($scope.listToSend.indexOf($scope.actualPermInRole[i].id) === -1) {
          $scope.listToSend.push($scope.actualPermInRole[i].permission_id)
          $scope.selectPermObj[$scope.actualPermInRole[i]['permission_id']] = $scope.actualPermInRole[i]
        }
      }
      $scope.checkInActual = function(id) {
        var actualPermList = []
        $scope.actualPermInRole.forEach(function(elem) {
          actualPermList.push(elem.permission_id)
        })
        if (actualPermList.indexOf(id) == -1) {
          return true
        } else {
          return false
        }
      }
    }, function errorCallback(response) {
      $scope.msg.deleteError('ролі');
    })
  }

  $scope.deletePermFormRole = function(perm) {
    $scope.actualPermInRole.forEach(function(actual_perm, index) {
      if (actual_perm.permission_id === perm.permission_id) {
        $scope.actualPermInRole.splice(index, 1)
        $scope.listToSend.splice($scope.listToSend.indexOf(perm.permission_id), 1)
      }
    })
  }

  $scope.searchWord = "";
  $scope.searchWordActual = "";
  $scope.bindResPerm = function() {
    $http({
      method: "PUT",
      url: "/api/role_permissions",
      data: {
        "role_id": $scope.rolePermObj.id,
        "permission_id": $scope.listToSend
      }
    }).then(function successCallback(data) {
      $scope.msg.editSuccess('прав');
      $scope.rolePermTable = true
      $scope.rolePermBlock = false
    }, function errorCallback(response) {
      $scope.msg.editError('прав');
    })
  }
}])
