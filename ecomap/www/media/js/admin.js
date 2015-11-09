var admin=angular.module("admin",[])

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

})
