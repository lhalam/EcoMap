app.controller('FaqTableCtrl', ['$scope', '$http', 'toaster', function($scope, $http, toaster){
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

    $scope.deletePage = function(page_id){
        $http({
            method: 'DELETE',
            url: '/api/deleteResource/' + page_id
        }).then(function successCallback(responce){
            console.log(responce);
            toaster.pop('success', 'Інструкцію видалено', 'Інструкцію було успішно видалено!');
            $scope.loadData();
        },
            function errorCallback(){})
    }

}])