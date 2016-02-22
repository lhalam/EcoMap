app.controller('ProblemCtrl', ['$scope', '$http', 'toaster', 'msg', 'msgError', 'Upload',
  function($scope, $http, toaster,  msg, msgError, Upload) {

    $scope.msg = msg;
    $scope.msgError = msgError;

    $scope.newProblemType = {};

    $scope.addProblemTypeModal = false;
    $scope.showAddPpoblemTypeModal = function() {
      $scope.addProblemTypeModal = true;
    };

    $scope.addProblemSubmit = function(newProblemType) {
      Upload.upload({
      url: '/api/problem_type',
      method: 'POST',
      cache: false,
      headers: {
        'Cache-Control': 'no-cache'
      },
      data: {
        file: newProblemType.picFile,
        problem_type_name: newProblemType.name,
        problem_type_radius: newProblemType.radius
      }
      }).then(function successCallback(data) {
        $scope.loadProblemType();
        $scope.addProblemTypeModal = false;
        $scope.msg.createSuccess('типу проблеми');
        $scope.newProblemType = {};
      }, function errorCallback(response) {
        $scope.addProblemTypeModal = false;
        if (arguments[0]['data']['msg']=='Name already taken')
          $scope.msg.createError('типу проблеми', $scope.msgError['alreadyExist']);
        if (arguments[0]['data']['msg']=='Incorrect data')
          $scope.msg.createError('типу проблеми', $scope.msgError['incorectData']);
         if (arguments[0]['data']['msg']=='Incorrect photo')
          $scope.msg.createError('типу проблеми', $scope.msgError['incorrectPhoto']);
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
      Upload.upload({
      url: '/api/problem_type',
      method: 'PUT',
      cache: false,
      headers: {
        'Cache-Control': 'no-cache'
      },
      data: {
        file: editProblemTypeObj.picFile,
        problem_type_name: editProblemTypeObj.name,
        problem_type_radius: editProblemTypeObj.radius,
        problem_type_id: editProblemTypeObj.id,

      }
      }).then(function successCallback(data) {
        $scope.loadProblemType();
        $scope.editProblemTypeModal = false;
        $scope.msg.editSuccess('типу проблеми');
      }, function errorCallback(response) {
        if (arguments[0]['data']['msg']=='Incorrect data')
          $scope.msg.createError('типу проблеми', $scope.msgError['incorectData']);
        if (arguments[0]['data']['msg']=='Wrong data')
          $scope.msg.createError('типу проблеми', $scope.msgError['incorrectPhoto']);
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
