app.controller('RestorePasswordCtrl', ['$scope', '$state', '$http', '$location', 'msg', 'toaster',
  function($scope, $state, $http, $location, msg, toaster) {
    $scope.restore = {};
    $scope.msg = msg;
    $scope.sendEmail = function(restore){
        if(!$scope.restore.email){
            return;
        }

        $http({
            method: 'POST',
            url: '/api/restore_password',
            data: $scope.restore
        }).then(function successCallback(response){
            $scope.msg.sendSuccess('імейлу')
        }, function errorCallback(){
            $scope.msg.sendError('імейлу')
        })
    };

    // $scope.checkHashSum = function(){
    //     $http({
    //         method: 'GET',
    //         url: '/api/url' + $state.params['hash_sum']
    //     }).then(function successCallback(response){
    //         //do what you need here
    //     }, function errorCallback(){
    //         //error callback if you need
    //     })
    // }

    // if($state.params['hash_sum']){
    //     $scope.checkHashSum();        
    // }

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
        window.location.href = 'http://ecomap.new:81/#/login'
      }, function errorCallback(){
        //error callback if you need
      })
    }
  }
]);