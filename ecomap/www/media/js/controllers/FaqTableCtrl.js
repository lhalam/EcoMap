app.controller('FaqTableCtrl', ['$scope', '$http', function($scope, $http){
    $scope.loadData = function(){
        $http({
            url: '/api/getTitles',
            method: 'GET'
        }).then(function successCallback(responce){
            $scope.pages = responce.data;
        },
            function errorCallback(){});
    };
    $scope.loadData();

    $scope.changeShowing = function(index){
        var data = {};
        $http({
            url: '/api/resources/'+$scope.pages[index].alias,
            method: 'GET'
        })
        .then(function successCallback(responce){
            data = responce.data[0];
            data.is_enabled = $scope.pages[index].is_enabled;
            
            $http({
                method: 'PUT',
                url: '/api/editResource/' + $scope.pages[index].id,
                data: data
            }).then(
                function successCallback(responce){
                    $scope.loadData();
                },
                function errorCallback(){}
            );
        },
            function errorCallback(){});
    };

}])