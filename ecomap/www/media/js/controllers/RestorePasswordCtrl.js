controller('RestorePasswordCtrl', ['$scope', '$state', '$http',
  function($scope, $state, $http) {

    $scope.restore = {};
    $scope.sendEmail = function(restore){
        if(!restore.email){
            return;
        }

        $http({
            method: 'POST',
            url: '/api/url',
            data: $scope.restore
        }).then(function successCallback(response){
            //do what you need here
        }, function errorCallback(){
            //error callback if you need
        })
    };

    $scope.checkHashSum = function(){
        $http({
            method: 'GET',
            url: '/api/url' + $state.params['hash_sum']
        }).then(function successCallback(response){
            //do what you need here
        }, function errorCallback(){
            //error callback if you need
        })
    }

    if($state.params['hash_sum']){
        $scope.checkHashSum();        
    }

    $scope.newPass = {};
    $scope.updatePass = function(pass){
        if(!pass.pass || !pass.confirmPass){
            return;
        }

        $http({
            method: 'POST',
            url: '/api/url',
            data: pass
        }).then(function successCallback(response){
            //do what you need here
        }, function errorCallback(){
            //error callback if you need
        })
    }
  }
]);