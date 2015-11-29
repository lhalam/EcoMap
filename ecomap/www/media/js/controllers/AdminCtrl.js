app.controller('AdminCtrl', ['$scope','$http', 'toaster',"$rootScope", function($scope,$http, toaster,$rootScope){

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