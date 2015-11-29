app.controller("ResourceCtrl",['$scope','$http', 'toaster','msg', function($scope,$http, toaster,msg){
    $scope.msg=msg
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
        $scope.newResource = {};
    };
    $scope.editResModal = false;

    $scope.showeditResModal = function(name,id){
        $scope.editResObj={
            'name':name,
            'id':id
        };
        $scope.editResModal = true;
    }


    $scope.editResource = function(editResObj){
        if(!editResObj.name || !editResObj.id){
            return;
        }

        $http({
        method:"PUT",
        url:"/api/resources",
        data:{
          "resource_name": editResObj['name'],
          "resource_id" :  editResObj['id']
        }
        }).then(function successCallback(data) {
            $scope.loadRes()
            $scope.editResModal = false;
            $scope.msg.editSuccess('ресурсу');
        }, function errorCallback(response) {
            $scope.msg.editError('ресурсу');
        })

    };


    $scope.deleteResource = function(id){
        $http({
          method:"DELETE",
          headers: {"Content-Type": "application/json;charset=utf-8"},
          url:"/api/resources",
          data:{
            "resource_id":id
          }
        }).then(function successCallback(data) {
            $scope.loadRes()
            $scope.msg.deleteSuccess('ресурсу');
        }, function errorCallback(response) {
            $scope.msg.deleteError('ресурсу');
        })
    };

    $scope.newResource = {};

    $scope.addResource = function(newResource){
        if(!newResource.name){
            return;
        }

         $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': $scope.newResource.name
            }
        }).then(function successCallback(data) {
        $scope.addResModal = false;
        $scope.Resources[data.data.added_resource]=data.data.resource_id
        $scope.addResModal=false
        $scope.msg.createSuccess('ресурсу');
        }, function errorCallback(response) {
            $scope.addResModal=false
            $scope.msg.createError('ресурсу');
        });

    };
}])