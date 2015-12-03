app.controller('detailedProblemCtrl', ['$scope', '$rootScope', '$state', '$http', 'toaster',
  function($scope, $rootScope, $state, $http, toaster) {
    $scope.photos = [];
    $scope.maxSeverity = [1, 2, 3, 4, 5];
    $http({
      "method": "GET",
      "url": "/api/problem_detailed_info/" + $state.params['id']
    }).then(function successCallback(data) {
      $rootScope.selectProblem = data.data[0][0];
      console.log(data.data);
      $rootScope.photos = data.data[0][2];
      console.log($rootScope.selectProblem);
      console.log($rootScope.photos);
      $rootScope.mapParams = {
        center: {
          latitude: $rootScope.selectProblem['latitude'],
          longitude: $rootScope.selectProblem['longitude']
        },
        zoom: 17
      };
      console.log($rootScope.selectProblem)
    }, function errorCallback(error) {});

    $scope.close = function() {
      $state.go('map')
    };

    $scope.getStatus = function(status) {
      var statuses = {
        'Unsolved': 'Не вирішено',
        'Solved': 'Вирішено'
      };
      return statuses[status];
    }
    $scope.getProblemType = function(type_id) {
    var types = {
      1: 'Проблеми лісів',
      2: 'Сміттєзвалища',
      3: 'Незаконна забудова',
      4: 'Проблеми водойм',
      5: 'Загрози біорізноманіттю',
      6: 'Браконьєрство',
      7: 'Інші проблеми'
    };
    return types[type_id];
  };
  }
]);