app.controller("PermisionCtrl",['$scope','$http', 'toaster','msg', function($scope,$http, toaster,msg){
    $scope.addPermModal = false;
    $scope.msg=msg;

    $scope.showAddPermModal = function(){
        $scope.addPermModal = true;
        $scope.perm = {};
    };
    $scope.show=function(){
       var name= $scope.perm.resource_name
    }
 
    $scope.addPermSubmit = function(){
        var id= $scope.Resources[$scope.perm.resource_name]

        $http({
            method:"POST",
            headers: {"Content-Type": "application/json;"},
            url:"/api/permissions",
            data:{
            "resource_id":id,
            "action":$scope.perm['action'],
            "modifier":$scope.perm['modifier'],
            "description":$scope.perm['description']
            } 
        }).then(function successCallback(data) {
            $scope.loadPerm()
            $scope.addPermModal = false;
            $scope.msg.createSuccess('права');
        }, function errorCallback(response) {
            $scope.msg.createError('права');

        });
    };

    $scope.editPermModal = false;
    $scope.showEditPermModal = function(perm){
        $scope.editPerm=perm
        $scope.editPermModal = true;
    }
    
    $scope.editPermSubmit = function(id){
         $http({
            method:"PUT",
            url:"/api/permissions",
            data:{
                "permission_id":$scope.editPerm.permission_id,
                "action":$scope.editPerm['action'],
                "modifier":$scope.editPerm.modifier, 
                "description":$scope.editPerm['description']
            }
        }).then(function successCallback(data) {
                $scope.editPermModal = false;
                $scope.msg.editSuccess('права');
                $scope.loadPerm()

            }, function errorCallback(response) {
                $scope.msg.editError('права');
            })
    };
    $scope.deletePerm=function(perm){
        $http({
            'method':"DELETE",
            'headers': {"Content-Type": "application/json;charset=utf-8"},
            'url':"/api/permissions",
            "data":{
                "permission_id":perm.permission_id
            }
            }).then(function successCallback(data) {
            if(!data.data.error){
                $scope.loadPerm()
                $scope.msg.deleteSuccess('права');
                }
            else{
                $scope.msg.deleteError('права');
            }
            }, function errorCallback(response) {
                 $scope.msg.deleteError('права');
            })
    }
}])