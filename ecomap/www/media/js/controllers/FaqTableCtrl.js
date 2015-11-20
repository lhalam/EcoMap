app.controller('FaqTableCtrl', ['$scope', '$http', function($scope, $http){
    $http({
        url: '/api/getTitles',
        method: 'GET'
    }).then(function successCallback(responce){
        $scope.pages = responce.data;
    },
            function errorCallback(){});

    $scope.changeShowing = function(id){
        // changes value of checkbox
    };

}])