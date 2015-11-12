var admin=angular.module("admin",[])


admin.controller("mainCtrl", function ($scope, $http) {
    $scope.resourceShow = false
    $scope.permisShow = false
    $scope.acceptedData
    
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
    }
    $scope.loadPermis = function () {
        console.log("click")
        $scope.permisShow = !$scope.permisShow
         $http({
                method: "GET",
                url: '/api/permissions',
                params: {
                    'resource_id': 1
                }
            }).then(function successCallback(data) {
                $scope.selectedResObj['permissions']=data
            }, function errorCallback(response) {
                console.log(response)
            })
    } 
/*
admin.controller("tableCtrl",function ($scope,$rootScope){

    $scope.acceptedData={'cabinet': {'put': {'user': 'None', 'admin': 'own'},
                     'get': {'user': 'own', 'admin': 'any'},
                     'post': {'user': 'any', 'admin': 'None'}},
       'page': {'get': {'user': 'any', 'admin': 'any'},
                 'post': {'user': 'None', 'admin': 'any'}},
         'page2': {'get': {'user': 'any', 'admin': 'any'},
                  'post': {'user': 'None', 'admin': 'any'},}
                  ,
         'page3': {'get': {'user': 'any', 'admin': 'any'},
                  'post': {'user': 'None', 'admin': 'any'},}
              }
  $scope.items=["a","b","c"]           
  $scope.TableData={}
  $scope.roles={

  }
  $scope.meth_obj={
    "1":"get",
    "2":"put",
    "3":"post",
    "4":'deleted'
  }
  $scope.permisions_obj={
    '1':'None',
    '2':'own',
    "3":"any"
  }

    $scope.parse = function(){
        acceptedData=$scope.acceptedData
        for (resource in acceptedData){
            resourceObj={}  
            //resourceObj['method_roles']={};       
            for(method in acceptedData[resource]){  
                var methodObj={}    
                for(role in  acceptedData[resource][method]){
                    methodObj[role]=acceptedData[resource][method][role]
          $scope.roles[role]=role   
                    //resourceObj['method_roles'][role]=role    
                }
                resourceObj[method]=methodObj
            }
            $scope.TableData[resource]=resourceObj
        }
    console.log($scope.roles)
    }
    $scope.show=function () {
        $scope.parse()
        
        
    }
    $scope.printTable=function(){
        console.log($scope.TableData)
    }
    $scope.addRole=function(new_role){
        $scope.roles[new_role]=new_role
    for(res in $scope.TableData)
      {
      for (meth in $scope.TableData[res]) {
        //console.log($scope.TableData[res])
       $scope.TableData[res][meth][new_role]="None"
      }
    }

    }
  $scope.creatResourse=function(res_name,res_method){
    $scope.TableData[res_name]={}
    $scope.TableData[res_name][res_method]={}
    //console.log( $scope.roles.length)
    for(role in $scope.roles){
      $scope.TableData[res_name][res_method][role]="None"
    }
   
  }
  $scope.addMeth=function(resource_name,meth_name){
    for (meth in $scope.TableData[resource_name]){
      console.log("this is method"+meth+" this is bool"+$scope.TableData[resource_name].hasOwnProperty(meth_name))
      if(!$scope.TableData[resource_name].hasOwnProperty(meth_name)){
          $scope.TableData[resource_name][meth_name]={}
          for (role in $scope.roles) {
          $scope.TableData[resource_name][meth_name][role]="None"
          console.log($scope.TableData)
          }
      }
      else {
        console.log("already has")
      }
    }
      

  }
  $scope.removeMeth=function(resource_name,remove_meth_name){
    for (meth in $scope.TableData[resource_name]){
      //console.log("this is method"+meth+" this is bool"+$scope.TableData[resource_name].hasOwnProperty(meth_name))
      if($scope.TableData[resource_name].hasOwnProperty(remove_meth_name)){
          delete $scope.TableData[resource_name][remove_meth_name]
        }
      else{
        console.log("does`n exist")
      }
      }
     
    }
  $scope.removeRes=function(remove_res){
>>>>>>> 87e1910345eb166bd51402fb76511c0b68a898e2

    for (resour in $scope.TableData){
      //console.log("this is method"+meth+" this is bool"+$scope.TableData[resource_name].hasOwnProperty(meth_name))
      if($scope.TableData.hasOwnProperty(remove_res)){
          delete $scope.TableData[remove_res]
        }
      else{
        console.log("does`n exist")
        }
      }
   
  }

    }*/

})