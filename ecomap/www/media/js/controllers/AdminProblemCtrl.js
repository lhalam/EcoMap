app.controller('ProblemCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError',
  function($scope, $http, toaster,  msg, msgError) {
    
    $scope.msg = msg;
    $scope.msgError = msgError;
    $scope.addProblemTypeModal = false;
    $scope.showAddPpoblemTypeModal = function() {
      $scope.addProblemTypeModal = true;
      $scope.problemType = {};
    };


    $scope.editProblemTypeModal = false;
    $scope.showEditPpoblemTypeModal = function(problemObj) {
      $scope.problemType = problemObj;
      console.log(problemObj);
      $scope.editProblemTypeModal = true;
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
