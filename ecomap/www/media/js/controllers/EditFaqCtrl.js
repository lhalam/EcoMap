app.controller('EditFaqCtrl', ['$scope', '$stateParams', '$http', 'toaster', '$state', function($scope, $stateParams, $http, toaster, $state){
    $scope.page = {};

    $scope.editPage = function(page){
        console.log(page);
        $http({
            method: 'PUT',
            url: '/api/editResource/' + page.id,
            data: page
        }).then(function successCallback(response){            
            toaster.pop('success', 'Інструкцію відредаговано', 'Інструкцію відредаговано успішно!');
            $state.go('user_profile');
        },
        function errorCallback(){
            toaster.pop('error', 'Помилка', 'Інструкцію не вдалось відредагувати через помилку!');
        });
    };

    $scope.loadPage = function(alias){
        $http({
            method: 'GET',
            url: '/api/resources/' + alias
        }).then(function successCallback(response){
            $scope.page.title = response.data[0].title;
            $scope.page.alias = response.data[0].alias;
            $scope.page.description = response.data[0].description;
            $scope.page.content = response.data[0].content;
            $scope.page.meta_keywords = response.data[0].meta_keywords;
            $scope.page.meta_description = response.data[0].meta_description;
            $scope.page.is_enabled = response.data[0].is_enabled;
            $scope.page.id = response.data[0].id;
        },
            function errorCallback(){})
    };

    $scope.loadPage($stateParams.alias);
}]);
