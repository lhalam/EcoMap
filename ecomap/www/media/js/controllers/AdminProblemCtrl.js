app.controller('ProblemCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster,  msg, msgError) {
    
    $scope.msg = msg;
    $scope.msgError = msgError;
    $scope.addProblemTypeModal = false;
    $scope.showAddPpoblemTypeModal = function() {
      $scope.addProblemTypeModal = true;
      $scope.problemType = {};
    };

    
    $scope.showEditProblemTypeModal= function(id, picture, name, radius) {
      $scope.editProblemTypeObj = {
        'id': id,
        'picture': picture,
        'name': name,
        'radius': radius
      };
      console.log($scope.editProblemTypeObj);
      $scope.editProblemTypeModal = true;
    }
    $scope.editProblemSubmit = function(editProblemTypeObj){
      if (!editProblemTypeObj.name || !editProblemTypeObj.radius) {
        $scope.msg.editError('типу проблеми', $scope.msgError['incorectData']);
        return;
      }
      console.log($scope.editProblemTypeObj);
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
        $scope.editProblemTypeModal = false;
        $scope.msg.editSuccess('типу проблеми');
      }, function errorCallback(response) {
        $scope.msg.editError('типу проблеми', $scope.msgError['alreadyExist']);
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
        $scope.msg.deleteSuccess('типу проблеми');
      }, function errorCallback(response) {
        $scope.msg.deleteError('типу проблеми', $scope.msgError['alreadyBinded']);
      })
    };

  }])
