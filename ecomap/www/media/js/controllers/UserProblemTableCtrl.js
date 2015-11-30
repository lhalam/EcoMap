app.controller('UserProblemTableCtrl', ['$scope', '$http', '$cookies', function($scope, $http, $cookies) {
  $scope.getProblemType = function(type_id){
    var types = {
        1: 'Проблеми лісів',
        2: 'Сміттєзвалища',
        3: 'Незаконна забудова',
        4: 'Проблеми водойм',
        5: 'Загрози біорізноманіттю',
        6: 'Браконьєрство',
        7: 'Інші проблеми'
    }
    return types[type_id];
  };

  $scope.getStatus = function(status){
    var statuses = {
        'Unsolved': 'Не вирішено',
        'Solved': 'Вирішено'
    };
    return statuses[status];
  }

  $scope.parseDate  = function(timestamp){
      // todo make here parse format logic fro timestamp
    var date = new Date(timestamp*1000).toString("H:mm MMM dd yyyy");
    return date
  };

  $scope.loadProblems = function(user_id) {
    $http({
      method: 'GET',
      url: 'api/usersProblem/' + user_id
    }).then(function successCallback(response) {
      $scope.problems = response.data;
    });
  }

  $scope.loadProblems($cookies.get('id'));

  $scope.detailedInfoModal = false;
  $scope.triggerDetailModal = function(problem_id){
    $scope.detailedInfoModal = !$scope.detailedInfoModal;
    $http({
        method: 'GET',
        url: '/api/problem_detailed_info/' + problem_id
    }).then(function successCallback(response){
        $scope.detailedProblem = response.data[0][0];
        console.log($scope.detailedProblem);
    })
  }
}])