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
    // $scope.loadProblems = function() {
    // $scope.problems = [];
    // $http({
    //   method: 'GET',
    //   url: '/api/problems'
    // }).then(function successCallback(response) {
    //   for (var i = 0; i < response.data.length; i++){
    //       $scope.problems.push(response.data[i]);
    //     }
    //   // console.log($scope.problems);
    //   }, function errorCallback() {})
    // };

    $scope.loadProblemType = function() {
      $scope.problemTypes =  [];
      $http({
        method: 'GET',
        url: '/api/problem_type',
      }).then(function successCallback(data) {
         for (var i = 0; i < data.data.length; i++){
          $scope.problemTypes.push(data.data[i]);
          $scope.problemTypes[i]['picture'] = '/image/markers/' + $scope.problemTypes[i]['picture'];
        }
          $scope.createGroups();
      }, function errorCallback(response) {})
    };
  $scope.loadProblemType();
    $scope.createGroups = function(){
      $scope.groups_list = [];
      for(var i = 0; i < $scope.problemTypes.length; i++){
        var group = {id:$scope.problemTypes [i]['id'], content:'<img src="' + $scope.problemTypes [i]['picture'] +'\"' +  ' style="width: 35px; height: 50px;'+'\">'};
        $scope.groups_list.push(group);
      }
    $http({
      method: 'GET',
      url: '/api/problems'
    }).then(function successCallback(response) {
      console.log(response);
        $scope.problems = [];
        $scope.start_date = response.data[0]['date']*1000.0;
      for (var i = 0; i < response.data.length; i++){
        response.data[i]['date']*=1000.0;
        var item = {id:response.data[i]['problem_id'], content:'', start: new Date(response.data[i]['date']),
          group:response.data[i]['problem_type_Id']};
          $scope.problems.push(item);
          if ($scope.start_date>response.data[i]['date'])
            $scope.start_date = response.data[i]['date'];
        }
        $scope.createPlot($scope.groups_list, $scope.problems);
      }, function errorCallback() {})
    };
  $scope.createPlot = function(groups_content, items_content){
    var container = document.getElementById('visualization');
    var groups = new vis.DataSet(groups_content);
    var items = new vis.DataSet(items_content);
    console.log( new Date($scope.start_date ));
    //   // Configuration for the Timeline
    var date = new Date();
    date.setDate(date.getDate() + 3);
      var options = {
        stack:false,
        min:new Date($scope.start_date - 60*60*12*2*1000),
        max: date,
        zoomMin: 1000*60*60*24*31,
        zoomMax:1000*60*60*24*31*12,
        orientation: 'top',
        showCurrentTime:false,
        locale: 'nl'
      };

  // Create a Timeline
  var timeline = new vis.Timeline(container, items, options);
   timeline.setGroups(groups);
    };
    $scope.loadCountSubs();
    $scope.loadSeverityStat();
    $scope.loadAllStatistic();
    $scope.loadProbCommStats();
}]);


