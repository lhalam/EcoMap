app.controller('RestorePasswordCtrl', ['$scope', '$state', '$http', '$rootScope', '$location', 'msg', 'toaster',
  function($scope, $state, $http, $rootScope, $location, msg, toaster) {
    $scope.restore = {};
    $scope.msg = msg;
    console.log("sdddddddddd");
    console.log(window.location);
    $rootScope.isFetching=false;
    $scope.sendEmail = function(restore){
        if(!$scope.restore.email){
            return;
        }
        $rootScope.isFetching=true;
        $http({
            method: 'POST',
            url: '/api/restore_password',
            data: $scope.restore
        }).then(function successCallback(response){
            window.location.href += '/#/login';
            $scope.msg.sendSuccess('імейлу');
            $rootScope.isFetching=false;
        }, function errorCallback(){
            $rootScope.isFetching=false;
            $scope.msg.sendError('імейлу')
        })
    };

    $scope.newPass = {};
    $scope.updatePass = function(pass){
      hash_sum = window.location.href.split('/')[5];
      if(!pass.pass || !pass.confirmPass){
          return;
      }
      $http({
        method: 'PUT',
        url: '/api/restore_password',
        data: {
          password: pass.pass,
          confirm_pass: pass.confirmPass,
          hash_sum: hash_sum.slice(0, -1)
        }
      })
      .then(function successCallback(response){
        //$state.go('login');
        window.location.href += '/#/login';
      }, function errorCallback(){
      })
    }
  }
]);
