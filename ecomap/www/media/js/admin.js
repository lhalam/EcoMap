var admin=angular.module("admin",[])

admin.controller("tableCtrl",function ($scope){
	$scope.acceptedData={'cabinet': {'put': {'user': 'None', 'admin': 'own'},
                     'get': {'user': 'own', 'admin': 'any'},
                     'post': {'user': 'any', 'admin': 'none'}},
         'page': {'get': {'user': 'any', 'admin': 'any'},
                  'post': {'user': 'None', 'admin': 'any'}},
         'page2': {'get': {'user': 'any', 'admin': 'any'},
                  'post': {'user': 'None', 'admin': 'any'}}
              }
    $scope.TableData={}
 	$scope.parse = function(){
 		acceptedData=$scope.acceptedData
 		for (resource in acceptedData){
 			resourceObj={} 	
 			resourceObj['method_roles']={};		
 			for(method in acceptedData[resource]){
 				
 				var methodObj={}
 				
 				for(role in  acceptedData[resource][method]){
 					methodObj[role]=acceptedData[resource][method][role]
					
					resourceObj['method_roles'][role]=role
 					
  				}
 				resourceObj[method]=methodObj
 			}
 			$scope.TableData[resource]=resourceObj
 		}

 	}
 	$scope.show=function () {
 		$scope.parse()
 		$scope.exaplme=$scope.TableData["cabinet"]
 		
 	}
 	$scope.printTable=function(){
 		console.log($scope.TableData)
 	}
 	$scope.addRole=function(resource_name,new_role){
 		$scope.TableData[resource_name]['method_roles'][new_role]=new_role
 		for (meth in $scope.TableData[resource_name]){
 			if(meth!=="method_roles"){
 				$scope.TableData[resource_name][meth][new_role]="None"
 				console.log($scope.TableData[resource_name][meth])
 			}
 			
 		}
 	

 	}


})
