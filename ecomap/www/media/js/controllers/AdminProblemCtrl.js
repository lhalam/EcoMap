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

    var user = [{"id": 1, "problem_type": "forest", "radius": 100, "img": "1.png"},
            {"id": 2, "problem_type": "lake", "radius": 100, "img": "2.png"},
            {"id": 3, "problem_type": "fhkj", "radius": 100, "img": "3.png"},
            {"id": 4, "problem_type": "jhgh", "radius": 100, "img": "4.png"}];

    $scope.selectedProblems = user;

  }])
