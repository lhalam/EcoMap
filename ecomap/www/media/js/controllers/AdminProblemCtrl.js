app.controller('ProblemCtrl', ['$scope', '$http', 'toaster', '$rootScope', 'msg',
  function($scope, $http, toaster, $rootScope, msg) {

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

  }])
