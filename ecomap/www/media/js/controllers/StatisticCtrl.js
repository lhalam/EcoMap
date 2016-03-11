app.controller('StatisticCtrl', ['$scope', '$http', '$state', '$cookies', '$window',
  function($scope, $http, $state, $cookies, $window) {
    $scope.period = 0;
    $scope.chartObject = {};
    $scope.chartObject.options = {
        colors: ['rgb(9, 91, 15)', 'rgb(35, 31, 32)', 'rgb(152, 68, 43)', 'rgb(27, 154, 214)', 'rgb(113, 191, 68)', 'rgb(255, 171, 9)', 'rgb(80, 9, 91)']
};
    $scope.chartObject.type = "PieChart";
    $scope.chartObject.data = {"cols": [
        {id: "t", label: "Topping", type: "string"},
        {id: "s", label: "Slices", type: "number"}
    ]};
    
    $scope.loadStatisticPieChart = function() {
      $scope.$watch('period', function(newValue){
          $scope.chartObject.data["rows"] = [];
          $http({
            method: 'GET',
            url: '/api/statisticPieChar',
            params: {
                    date: newValue,
                  }
          }).then(function successCallback(data) {
            $scope.statistic = data.data;
            $scope.statistic.forEach(function(item){
              $scope.chartObject.data["rows"].push({c: [{v: item['type']},
                                                        {v: item['count']}]})
            });                                
          }, function errorCallback(response) {})
      })
    }
    $scope.loadStatisticPieChart()

}]);
    
