app.controller('UserProfileCtrl', ['$scope', '$state', '$cookies', '$http', 'toaster', 'Upload', '$timeout',
  function($scope, $state, $cookies, $http, toaster, Upload, $timeout) {

    $scope.user = {};
    $scope.user.id = $cookies.get("id");

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
    $scope.changePassword = function(passwd) {
      console.log(passwd);
      if(!passwd.old_pass || !passwd.new_pass || !passwd.new_pass_confirm){
        return;
      }

      var data = {};
      data.id = $cookies.get('id');
      data.old_pass = passwd.old_pass;
      data.password = passwd.new_pass;
      console.log(data);
      $http({
        method: 'POST',
        url: '/api/change_password',
        data: {
          'id':data.id,
          'old_pass':data.old_pass,
          'password': data.new_pass
        }
      }).then(function successCallback(responce) {
        passwd = {};
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
  }
]);
