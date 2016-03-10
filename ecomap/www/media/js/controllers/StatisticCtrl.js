app.controller('StatisticCtrl', ['$scope', '$http', '$state', '$cookies', '$window',
  function($scope, $http, $state, $cookies, $window) {
    $scope.chartObject = {};
    
    $scope.chartObject.type = "PieChart";
    
    $scope.chartObject.data = {"cols": [
        {id: "t", label: "Topping", type: "string"},
        {id: "s", label: "Slices", type: "number"}
    ]};
    $scope.chartObject.data["rows"] = [];

    $scope.loadStatistic = function() {
      $http({
        method: 'GET',
        url: '/api/statisticPieChar',
      }).then(function successCallback(data) {
        $scope.statistic = data.data;
        for(var i=0; i<$scope.statistic.length; i++){
          $scope.chartObject.data["rows"].push({c: [{v: $scope.statistic[i]['type']},{v: $scope.statistic[i]['count']}]})
        }                                  
      }, function errorCallback(response) {})
    }
    $scope.loadStatistic()

}]);
    
