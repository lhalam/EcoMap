app.controller('ProblemCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster,  msg, msgError) {

    $scope.msg = msg;
    $scope.msgError = msgError;
    $scope.addProblemTypeModal = false;
    $scope.showAddPpoblemTypeModal = function() {
      $scope.addProblemTypeModal = true;
      $scope.newProblemType = {};
    };

    $scope.newProblemType = {};
    $scope.addProblemSubmit = function(newProblemType) {
      if (!newProblemType.name) {
        return;
      }
      $http({
        method: 'POST',
        url: '/api/problem_type',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        data: {
          'problem_type_picture': $scope.newProblemType.picture,
          'problem_type_name': $scope.newProblemType.name,
          'problem_type_radius': $scope.newProblemType.radius
        }
      }).then(function successCallback(data) {
        $scope.loadProblemType();
        $scope.addProblemTypeModal = false;
        $scope.msg.createSuccess('типу проблеми');
        console.log(data);
      }, function errorCallback(response) {
        $scope.addProblemTypeModal = false;
        console.log(arguments[0]['data']['msg']);
        console.log(arguments);
        console.log(arguments[0]['data']['msg']);
        if (arguments[0]['data']['msg']=='Name already taken')
          $scope.msg.createError('типу проблеми', $scope.msgError['alreadyExist']);
        if (arguments[0]['data']['msg']=='Incorrect data')
          $scope.msg.createError('типу проблеми', $scope.msgError['incorectData']);
      });
    };


    $scope.showEditProblemTypeModal= function(id, picture, name, radius) {
      $scope.editProblemTypeObj = {
        'id': id,
        'picture': picture,
        'name': name,
        'radius': radius
      };
      $scope.editProblemTypeModal = true;
    }
    $scope.editProblemSubmit = function(editProblemTypeObj){
      if (!editProblemTypeObj.name || !editProblemTypeObj.radius) {
        $scope.msg.editError('типу проблеми', $scope.msgError['incorectData']);
        return;
      }
      $http({
        method: 'PUT',
        url: '/api/problem_type',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        data: {
          'problem_type_id': $scope.editProblemTypeObj['id'],
          'problem_type_picture': $scope.editProblemTypeObj['picture'],
          'problem_type_name': $scope.editProblemTypeObj['name'],
          'problem_type_radius': $scope.editProblemTypeObj['radius']
        }
      }).then(function successCallback(data) {
        $scope.loadProblemType();
        $scope.editProblemTypeModal = false;
        $scope.msg.editSuccess('типу проблеми');
      }, function errorCallback(response) {
        $scope.msg.editError('типу проблеми', $scope.msgError['incorectData']);
      })
    };

    $scope.deleteProblemType = function(id) {
      $http({
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        url: '/api/problem_type',
        data: {
          'problem_type_id': id
        }
      }).then(function successCallback(data) {
        $scope.loadProblemType();
        $scope.msg.deleteSuccess('типу проблеми');
      }, function errorCallback(response) {
        $scope.msg.deleteError('типу проблеми', $scope.msgError['alreadyBinded']);
      })
    };

  }])
