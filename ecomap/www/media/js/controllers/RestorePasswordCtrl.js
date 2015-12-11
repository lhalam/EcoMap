app.controller('RestorePasswordCtrl', ['$scope', '$state', '$http', '$location',
  function($scope, $state, $http, $location) {

    $scope.restore = {};
    $scope.sendEmail = function(restore){
        if(!$scope.restore.email){
            return;
        }

        $http({
            method: 'POST',
            url: '/api/restore_password',
            data: $scope.restore
        }).then(function successCallback(response){
            //do what you need here
        }, function errorCallback(){
            //error callback if you need
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
        window.location.href = 'http://134.249.141.35:81/#/login'
      }, function errorCallback(){
        //error callback if you need
      })
    }
  }
]);