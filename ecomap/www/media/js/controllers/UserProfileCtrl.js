app.controller('UserProfileCtrl', ['$scope', '$state', '$cookies', '$http', 'msg', 'toaster',
  function($scope, $state, $cookies, $http, msg, toaster, $auth) {
    $scope.user = {};
    $scope.user.id = $cookies.get("id");
    $scope.msg = msg;
    $scope.tabs = [
      {heading: "Профіль користувача", route: "user_profile.info", active: false, showToUser: true},
      {heading: "Мої проблеми", route: "user_profile.problems", active: false, showToUser: true},
      {heading: "Мої коментарі", route: "user_profile.comments", active: false, showToUser: true},
      {heading: "Мої підписки", route: "user_profile.subscriptions", active: false, showToUser: true},
      {heading: "Редагування F.A.Q.", route: "user_profile.faq", active: false, showToUser: false}
    ];
    $scope.$on("$stateChangeSuccess", function() {
      $scope.tabs.forEach(function(tab) {
        tab.active = $scope.active(tab.route);
      });
    });
    $scope.go = function(route) {
      $state.go(route);
    };
    $scope.active = function(route) {
      return $state.is(route);
    };
    if ($scope.user.id) {
      $http({
        url: '/api/user_detailed_info/' + $scope.user.id,
        method: 'GET'
      }).success(function(response) {
        $scope.user.data = response;
        $scope.user.data.avatar = $scope.user.data.avatar || 'http://placehold.it/150x150';
      });
    }
    $scope.password = {
      old_pass: "",
      new_pass: "",
      new_pass_confirm: ""
    };
    $scope.changePassword = function(passwd, form) {
      if(!passwd.old_pass || !passwd.new_pass || !passwd.new_pass_confirm) {
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
        form.$setUntouched();
        toaster.pop('success', 'Пароль', 'Пароль було успішно змінено!');

      }, function errorCallback(responce) {
        if (responce.status == 401 || responce.status == 400) {
          $scope.wrongOldPass = true;
        }
      });
    };  
    $scope.userDelete = function() {
      if (confirm("Ви бажаєте видалити користувача?")) {
      var data = {}
      $scope.msg = msg;
      data.id = $cookies.get('id');
      $http({
        method: "DELETE",
        headers: {
          "Content-Type": "application/json;charset=utf-8"
        },
        url: "/api/delete_user_request",
        data: {
          'user_id': data.id
        }
      }).then(function successCallback(response) {
            $scope.msg.sendSuccess('імейлу')
        }, function errorCallback() {
            $scope.msg.sendError('імейлу')
        })
       
    }};    
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
