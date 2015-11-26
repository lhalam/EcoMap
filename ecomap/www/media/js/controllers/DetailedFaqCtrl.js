app.controller('DetailedFaqCtrl', ['$scope', '$stateParams', '$state', '$http', function($scope, $stateParams, $state, $http){
    $http({
        url: '/api/resources/'+$stateParams.faqAlias,
        method: 'GET'
    }).then(function successCallback(responce){
        $scope.faqInfo = responce.data[0];
    },
    function errorCallback(){
        $state.go('error404');
    });
}]);
