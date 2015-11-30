app.controller('AdminCtrl', ['$scope', '$http', 'toaster', "$rootScope", 
  '$state', function($scope, $http, toaster, $rootScope, $state) {
    $scope.meth_obj = {
      "1": "GET",
      "2": "PUT",
      "3": "POST",
      "4": 'DELETE'
    }
    $scope.modif_obj = {
      '1': 'None',
      '2': 'Own',
      "3": "Any"
    }
    $scope.selectCountObj = {
      "1": '5',
      "2": "10",
      "3": "15",
      "4": "20"
    }
    $scope.selectCount = {
      'selected': "5"
    }

    $scope.tabs = [
      { heading: "Ресурси", route:"admin.resources", active:false },
      { heading: "Права", route:"admin.permissions", active:false },
      { heading: "Ролі", route:"admin.roles", active:false },
      { heading: "Користувачі", route:"admin.users", active:false }
    ];

    $scope.$on("$stateChangeSuccess", function() {
      $scope.tabs.forEach(function(tab) {
        tab.active = $scope.active(tab.route);
      });
    });

    $scope.go = function(route){
      $state.go(route);
    };

    $scope.active = function(route){
      return $state.is(route);
    };

    $scope.loadRes = function() {
      $http({
        method: 'GET',
        url: '/api/resources'
      }).then(function successCallback(data) {
        $scope.Resources = data.data
      }, function errorCallback(response) {});
    }

    $scope.loadPerm = function() {
      $http({
        method: "GET",
        url: '/api/all_permissions',
      }).then(function successCallback(data) {
        $scope.Permisions = data.data;
      }, function errorCallback(response) {})
    }

    $scope.loadRole = function() {
      $http({
        method: "GET",
        url: "/api/roles",
      }).then(function successCallback(data) {
        $scope.Roles = data.data
      }, function errorCallback(response) {})
    }
    
    $scope.loadData = function() {
      $scope.loadRole()
      $scope.loadRes()
      $scope.loadPerm()
    }
    $scope.loadData()
  }
]);