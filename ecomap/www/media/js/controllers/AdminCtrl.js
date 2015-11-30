app.factory('msgError', function (toaster) {
        return msgError = {
            "alreadyExist": " Дане ім’я вже зарезервоване.",
            "alreadyBinded": " Так як дані вже прив’язані .",
            "incorectData":" Так як дані невірні."
        }
    })
app.controller('AdminCtrl', ['$scope','$http', 'toaster',"$rootScope", function($scope,$http, toaster,$rootScope){
    // app.factory('msg', function (toaster) {
    // return msg = {
    //     editSuccess: function(msg){
    //         toaster.pop('success', 'Редагування', 'Редагування ' + msg + ' здійснено успішно!');
    //     },
    //     deleteSuccess: function(msg){
    //         toaster.pop('success', 'Видалення', 'Видалення ' + msg + ' здійснено успішно!');
    //     },
    //     createSuccess: function(msg){
    //         toaster.pop('success', 'Додавання', 'Додавання ' + msg + ' здійснено успішно!');
    //     },
    //     editError: function(msg,type){
    //         toaster.pop('error', 'Редагування', 'При редагуванні ' + msg + ' виникла помилка!'+type);
    //     },
    //     deleteError: function(msg,type){
    //         toaster.pop('error', 'Видалення', 'При видаленні ' + msg + ' виникла помилка!'+type);
    //     },
    //     createError: function(msg,type){
    //         toaster.pop('error', 'Додавання', 'При додаванні ' + msg + ' виникла помилка!'+type);
    //     },
    // };
    // });

    $scope.meth_obj={
        "1":"GET",
        "2":"PUT",
        "3":"POST",
        "4":'DELETE'
    }
    $scope.modif_obj={
        '1':'None',
        '2':'Own',
        "3":"Any"
    }
    
    $scope.selectCountObj={
        "1":'5',
        "2":"10",
        "3":"15",
        "4":"20"
    }
    $scope.selectCount={
        'selected':"5"
    }
    

    $scope.loadRes=function(){
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.Resources = data.data

        }, function errorCallback(response) {
        });
    }
    $scope.loadPerm=function(){
        $http({
                method: "GET",
                url: '/api/all_permissions',
               
            }).then(function successCallback(data) {
                $scope.Permisions=data.data;              

            }, function errorCallback(response) {
            })

    }
    $scope.loadRole=function(){
         $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
            },function errorCallback(response) {
            })

    }

    $scope.loadData=function(){
        $scope.loadRole()
        $scope.loadRes()
        $scope.loadPerm()

        }

    $scope.loadData()
}])