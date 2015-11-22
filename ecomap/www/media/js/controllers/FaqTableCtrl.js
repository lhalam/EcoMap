app.controller('FaqTableCtrl', ['$scope', '$http', 'toaster', function($scope, $http, toaster){
    $scope.loadData = function(){
        $http({
            url: '/api/getTitles',
            method: 'GET'
        }).then(function successCallback(response){
            $scope.pages = response.data;
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
        .then(function successCallback(response){
            data = response.data[0];
            data.is_enabled = $scope.pages[index].is_enabled;
            
            $http({
                method: 'PUT',
                url: '/api/editResource/' + $scope.pages[index].id,
                data: data
            }).then(
                function successCallback(response){
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
        }).then(function successCallback(response){
            toaster.pop('success', 'Інструкцію видалено', 'Інструкцію було успішно видалено!');
            $scope.loadData();
        },
        function errorCallback(){
            toaster.pop('error', 'Помилка при видаленні', 'Інструкцію не було видалено через помилку!');
        })
    }

}])