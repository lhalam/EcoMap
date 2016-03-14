app.controller('MapCtrl', ['$scope', '$http', '$rootScope', '$state', 'MapFactory',
  function($scope, $http, $rootScope, $state, MapFactory) {
    MapFactory.initMap();
    MapFactory.turnResizeOn();
    $scope.markers = MapFactory.loadProblems();
    $scope.filterTrigger = false;
    $scope.toogleFilter = function() {
      $scope.filterTrigger = !$scope.filterTrigger;
    }

     $scope.loadProblemType = function() {
      $scope.Types = {};
      $http({
        method: 'GET',
        url: '/api/problem_type_filtration',
      }).then(function successCallback(data) {
        var problemTypes = data.data;
         for (var i = 0; i < data.data.length; i++){
          $scope.Types[String(problemTypes[i]['id'])] = [problemTypes[i]['picture'], problemTypes[i]['name']];
        }
    $scope.Status = {
      'Unsolved': 'Не вирішена',
      'Solved': 'Вирішена'
    };
    $scope.selectedType = [];
    $scope.selectedStatus = [];
    for (type in $scope.Types) {
      $scope.selectedType.push(type)
    }
    for (s in $scope.Status) {
      $scope.selectedStatus.push(s)
    }
      }, function errorCallback(response) {})
    };
    $scope.loadProblemType();
    $scope.toggleType = function(type_id) {
      if ($scope.selectedType.indexOf(type_id + '') !== -1) {
        $scope.selectedType.splice($scope.selectedType.indexOf(type_id), 1)
      } else {
        $scope.selectedType.push(type_id);
      }
      $scope.filterMarker()
    }
    $scope.toggleStatus = function(status) {
      if ($scope.selectedStatus.indexOf(status) !== -1) {
        $scope.selectedStatus.splice($scope.selectedStatus.indexOf(status), 1);
      } else {
        $scope.selectedStatus.push(status)
      }
      $scope.filterMarker()
    }
    $scope.dt={}
    $scope.selectTime = function(marker) {
      if (!$scope.dt.to || !$scope.dt.from) {
        return false
      } else if (marker.date > $scope.dt.from.getTime() / 1000 && marker.date < $scope.dt.to.getTime() / 1000) {
        return false
      } else return true
    }
    $scope.filterMarker = function() {
      angular.forEach($scope.markers, function(marker, key) {
        if ($scope.selectedType.indexOf(marker.problem_type_Id + '') === -1 || $scope.selectedStatus.indexOf(marker['problemStatus']) === -1 || $scope.selectTime(marker)) {
          marker.setVisible(false);
        } else {
          marker.setVisible(true);
        }
      });
      MapFactory.refreshCluster();
    }
  }
]);
