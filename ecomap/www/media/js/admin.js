var admin=angular.module("admin",[])


admin.controller("mainCtrl", function ($scope, $http) {
    $scope.resourceShow = false
    $scope.permisShow = false
    $scope.acceptedData
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
    $scope.loadRes = function () {
        $scope.resourceShow = !$scope.resourceShow
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.acceptedData = data.data
            console.log($scope.acceptedData)
        }, function errorCallback(response) {
            console.log(response)
        });
    }

    $scope.addRes = function (newName) {
        console.log($scope.acceptedData)
        $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': newName
            }
        }).then(function successCallback(data) {
            var addedobject = data.data['added_resource']
            var addedId = data.data['resource_id']
            console.log(data.data)
            $scope.acceptedData[addedobject]=addedId
        }, function errorCallback(response) {
            console.log(response)
        });
    }

    $scope.deleteRes=function(id){
        console.log(id)
        $http({
          method:"DELETE",
          headers: {"Content-Type": "application/json;charset=utf-8"},
          url:"/api/resources",
          data:{
            "resource_id":id
          }
        }).then(function successCallback(data) {
            if(data.data['deleted_resource']){
                deletedResId=data.data['deleted_resource']
                for (name in $scope.acceptedData){
                if ($scope.acceptedData[name] === id){
                    console.log($scope.acceptedData[name])
                    delete $scope.acceptedData[name]
                }
            }
            }
            else{
               console.log('eroorrr') 
            }
            
            //console.log(data.data)
           //$scope.acceptedData=data.data
           
        }, function errorCallback(response) {
            console.log(response)
        })
    }
    $scope.editShow=function(){
       $scope.isEdit=!$scope.isEdit
    }
    $scope.editRes=function(name,id){
      console.log(id)
     
      $http({
        method:"PUT",
        url:"/api/resources",
        data:{
          "new_resource_name":name,
          "resource_id" : id
        }
      }).then(function successCallback(data) {
          $scope.editShow()
           console.log(data)
        }, function errorCallback(response) {
            console.log(response)
        })
    }
    $scope.selectedRes=function(name,id){
        $scope.selectedResObj={
            "name":name,
            "id":id
        }
        $http({
                method: "GET",
                url: '/api/permissions',
                params: {
                    'resource_id': id
                }
            }).then(function successCallback(data) {
                console.log(data.data)
                $scope.selectedResObj['permissions']=data.data
            }, function errorCallback(response) {
                console.log(response)
            })
              console.log($scope.selectedResObj)  
    }
    $scope.loadPermis = function () {
        console.log("click")
        $scope.permisShow = !$scope.permisShow
         $http({
                method: "GET",
                url: '/api/all_permissions',
               
            }).then(function successCallback(data) {
                $scope.allPermisions=data.data;
                console.log(data.data)
            }, function errorCallback(response) {
                console.log(response)
            })
    } 
    $scope.editPermis=function(permisObj){
        $scope.editPermisObj=permisObj;
        console.log($scope.editPermisObj['action'])

    }
    $scope.submitPermEdit=function(){
        $http({
            method:"PUT",
            url:"/api/permissions",
            data:{
                "permission_id":$scope.editPermisObj.permission_id,
                "new_action":$scope.editPermisObj['action'],
                "new_modifier":$scope.editPermisObj.modifier, 
                "new_description":$scope.editPermisObj['description']
            }
        }).then(function successCallback(data) {
                console.log(data.data)
            }, function errorCallback(response) {
                console.log(response)
            })
    }
        $scope.loadRole=function(){
            $scope.isRoleShow=!$scope.isRoleShow
            $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
                console.log(data.data)
            }, function errorCallback(response) {
                console.log(response)
            })

        }
        $scope.createRole=function(role){
            $http({
                method:"POST",
                url:"/api/roles",
                data:{
                    "role_name":role
                }
            }).then(function successCallback(data) {
                $scope.Roles[data.data.added_role]=data.data
                console.log(data.data)
            }, function errorCallback(response) {
                console.log(response)
            })
        }
        $scope.selectedRole=function(){

        }
})