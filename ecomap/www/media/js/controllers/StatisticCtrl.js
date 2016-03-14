app.controller('StatisticCtrl', ['$scope', '$http', '$state', '$cookies', '$window','toaster',
  function($scope, $http, $state, $cookies, $window, toaster) {
    $scope.period = 0;
    $scope.chartObject = {};
    $scope.chartObject.type = "PieChart";
    $scope.chartObject.data = {"cols": [
        {id: "t", label: "Topping", type: "string"},
        {id: "s", label: "Slices", type: "number"}
    ]};
    $scope.all_statistic = [{title: 'Проблем', count: ''},
                            {title: 'Підписок', count: ''},
                            {title: 'Коментарів', count: ''},
                            {title: 'Фотографій', count: ''}];
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
    $scope.loadCountSubs = function() {
        $http({
            method: 'GET',
            url: '/api/countSubscriptions',
        }).then(function successCallback(response) {
            $scope.subscriptions = response.data[0];
        })
    };
    $scope.loadSeverityStat = function() {
        $http({
            method: 'GET',
            url: '/api/problems_severity_stats',
        }).then(function successCallback(response) {
            $scope.severities = response.data;
        })
    };
    $scope.loadAllStatistic = function() {
        $http({
            method: 'GET',
            url: '/api/statistic_all',
        }).then(function successCallback(response) {
            for(var i=0; i<response.data.length; i++){
              $scope.all_statistic[i].count = response.data[i];
            }
        })
    };
    $scope.loadProbCommStats = function() {
        $http({
            method: 'GET',
            url: '/api/problems_comments_stats',
        }).then(function successCallback(response) {
            $scope.problCommStats = response.data
        }, function errorCallback (response){
            toaster.pop('error', 'Відправлення' , 'Сталась помилка');
        });
    };

    $scope.triggerDetailModal = function(problem_id) {
      var url = '/#/detailedProblem/' + problem_id;
      window.open(url, '_blank');
    };
    $scope.loadCountSubs();
    $scope.loadSeverityStat();
    $scope.loadAllStatistic();
    $scope.loadProbCommStats();
}]);
    

