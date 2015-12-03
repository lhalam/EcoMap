app.controller('UserProfileCtrl', ['$scope', '$state', '$cookies', '$http', 'toaster', 'Upload', '$timeout',
  function($scope, $state, $cookies, $http, toaster, Upload, $timeout) {

    $scope.user = {};
    $scope.user.id = $cookies.get("id");

    $scope.tabs = [
      { heading: "Профіль користувача", route:"user_profile.info", active:false, showToUser: true},
      { heading: "Мої проблеми", route:"user_profile.problems", active:false, showToUser: true },
      { heading: "Мої коментарі", route:"user_profile.comments", active:false, showToUser: true },
      { heading: "Редагування F.A.Q.", route:"user_profile.faq", active:false, showToUser: false }
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

    if ($scope.user.id) {
      $http({
        url: '/api/user_detailed_info/' + $scope.user.id,
        method: 'GET'
      }).success(function(response) {
        $scope.user.data = response;
        $scope.user.data.avatar = $scope.user.data.avatar || 'http://placehold.it/200x200';
      });
    }

    $scope.password = {
      old_pass: "",
      new_pass: "",
      new_pass_confirm: ""
    };
    $scope.changePassword = function(passwd) {
      if(!passwd.old_pass || !passwd.new_pass || !passwd.new_pass_confirm){
        return;
      }

      var data = {};
      data.id = $cookies.get('id');
      $http({
        method: 'POST',
        url: '/api/change_password',
        data: {
          'id': data.id,
          'old_pass': passwd.old_pass,
          'password': passwd.new_pass
        }
      }).then(function successCallback(responce) {
        $scope.password = {};
        toaster.pop('success', 'Пароль', 'Пароль було успішно змінено!');
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
}]);
