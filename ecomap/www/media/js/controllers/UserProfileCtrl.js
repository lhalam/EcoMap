app.controller('UserProfileCtrl', ['$scope', '$state', '$cookies', '$http', 'toaster', 'Upload', '$timeout',
  function($scope, $state, $cookies, $http, toaster, Upload, $timeout) {

    $scope.user = {};
    $scope.user.id = $cookies.get("id");
    $scope.body = angular.element(document.body);
    $scope.body.addClass("body-scroll-shown");

    if ($scope.user.id) {
      $http({
        url: '/api/user_detailed_info/' + $scope.user.id,
        method: 'GET'
      }).success(function(response) {
        $scope.user.data = response;
        $scope.user.data.avatar = $scope.user.data.avatar || 'http://placehold.it/150x150';
      });
    }

    $scope.selectedTab = "userInfo";
    $scope.setTab = function(tabName) {
      $scope.selectedTab = tabName;
    };

    $scope.isSelected = function(tabName) {
      return $scope.selectedTab == tabName;
    };

    console.log($scope);
    $scope.changePassword = function() {
      var data = {};
      data.id = $cookies.get('id');
      data.old_pass = $scope.password.old_pass;
      data.password = $scope.password.new_pass;
      console.log(data);
      $http({
        method: 'POST',
        url: '/api/change_password',
        data: data
      }).then(function successCallback(responce) {
        $scope.password = {};
        toaster.pop('success', 'Пароль', 'Пароль було успішно змінено!');
        $scope.changePasswordForm.$setUntouched();
      }, function errorCallback(responce) {
        if (responce.status == 401) {
          $scope.wrongOldPass = true;
        }
      });
    };

    $scope.redirect = function(state){
      $state.go(state);
    };

    $scope.wrongOldPass = false;
    $scope.getWrongPass = function() {
      return $scope.wrongOldPass;
    };

    $scope.changeWrongPass = function() {
      $scope.wrongOldPass = false;
    };

    $scope.alert = false;
    $scope.closeAlert = function() {
      $scope.alert = false;
    };

    $scope.showAlert = function() {
      return $scope.alert;
    };

    $scope.$on("$destroy", function handler() {
      $scope.body.removeClass("body-scroll-shown");
    });

  }
]);
