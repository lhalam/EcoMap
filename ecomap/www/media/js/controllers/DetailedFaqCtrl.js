app.controller('DetailedFaqCtrl', ['$scope', '$stateParams', '$http', function($scope, $stateParams, $http){
    $http({
        url: '/api/resources/'+$stateParams.faqAlias,
        method: 'GET'
    })
    .then(function successCallback(responce){
        $scope.faqInfo = responce.data[0];
        console.log(responce.data);
    },
        function errorCallback(){});
}]);