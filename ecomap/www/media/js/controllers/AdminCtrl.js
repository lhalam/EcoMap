app.controller('AdminCtrl', ['$scope','$http', function($scope,$http){

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
    $scope.role_obj={
        "1":"admin",
        "2":"moderator",
        "3":"user"
    }

    $scope.loadData=function(){

        //load resources
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.Resources = data.data

        }, function errorCallback(response) {
            console.log(response)
        });

        //load permisions
         $http({
                method: "GET",
                url: '/api/all_permissions',
               
            }).then(function successCallback(data) {
                $scope.Permisions=data.data;
                console.log($scope.Permisions)
                
            }, function errorCallback(response) {
                console.log(response)
            })

        // load roles

        $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
                console.log($scope.Roles)
            },function errorCallback(response) {
                console.log(response)
            })

        $http({
            method:'GET',
            url:"/api/user_roles"
        }).then(function successCallback(data) {
                //$scope.Roles=data.
                $scope.Users=data.data
                console.log("user_roles")
                console.log(data)
            },function errorCallback(response) {
                console.log(response)
            })

    }

    $scope.loadData()

	// resource section

    //trigers for modal windows
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
    };

    $scope.editResModal = false;

    $scope.showEditResModal = function(name,id){
        //create edit object for modal window
    	$scope.editResObj={
            'name':name,
    		'id':id
    	};
    	$scope.editResModal = true;
    }

    $scope.editResource = function(){
        $http({
        method:"PUT",
        url:"/api/resources",
        data:{
          "new_resource_name":$scope.editResObj['name'],
          "resource_id" : $scope.editResObj['id']
        }
        }).then(function successCallback(data) {

        }, function errorCallback(response) {
            $scope.addResModal=false
            $scope.Eror=response.data.error;
            $scope.customEror=true;
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
            //if accepted data has attribute  'deleted_resource',delete prop
            if(data.data['deleted_resource']){
                deletedResId=data.data['deleted_resource']
                for (name in $scope.Resources) {
                    if ($scope.Resources[name] === deletedResId){
                        delete $scope.Resources[name]
                    }
                }
            }
            else {
                    $scope.Eror=data.data['error']
                    $scope.customEror=true
                }        
        }, function errorCallback(response) {
            $scope.Eror=response.statusText
            $scope.customEror=true
        })
   	};

    //Create new resource object 

    $scope.newResource = {};
    var data = {
        'resource_name': $scope.newResource['name']

    }
    $scope.addResource = function(){
         $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': $scope.newResource.name
            }
        }).then(function successCallback(data) {
        // add resource to scope
        console.log($scope.newResource.name)
        $scope.Resources[data.data.added_resource]=data.data.resource_id
        $scope.addResModal=false
        }, function errorCallback(response) {
            console.log($scope.newResource.name)
            $scope.addResModal=false
            $scope.Eror=response.data.error
            $scope.customEror=true
        });
    };


    //permission section

    //Permision modal windows trigers
    $scope.addPermModal = false;
    $scope.showAddPermModal = function(){
    	$scope.addPermModal = true;
    };
    $scope.show=function(){
       var name= $scope.perm.resource_name
    }
    // create obj for new permision
    $scope.perm = {};
    $scope.addPermSubmit = function(){
        // get resorce id  from client chose in front end
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

        }, function errorCallback(response) {
            $scope.Eror=response.statusText
            $scope.customEror=true
        });
    };

    $scope.editPermModal = false;
    $scope.showEditPermModal = function(perm){
        $scope.editPerm=perm
    	$scope.editPermModal = true;
    }
    // function for editing permisions 
    
    $scope.editPermSubmit = function(id){
         $http({
            method:"PUT",
            url:"/api/permissions",
            data:{
                "permission_id":$scope.editPerm.permission_id,
                "new_action":$scope.editPerm['action'],
                "new_modifier":$scope.editPerm.modifier, 
                "new_description":$scope.editPerm['description']
            }
        }).then(function successCallback(data) {

            }, function errorCallback(response) {
                console.log(response)
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
                if(data.data.deleted_permission){
                    deletedResId=data.data['deleted_permission']
                    /* if permision success deleted , delete it from 
                       all local Permisions database*/
                    for (name in $scope.Permisions){
                        if ($scope.Permisions[name]['permission_id'] === perm.permission_id){
                        $scope.Permisions.length = $scope.Permisions.length-1
                        delete $scope.Permisions[name]
                        }

                    }   
                }
            else if(data.data['error']){
                    $scope.Eror=data.data['error']
                    $scope.customEror=true
                }
            }, function errorCallback(response) {
                $scope.Eror=response.statusText
                $scope.customEror=true
        })
    }

    // Role section

    $scope.addRoleModal = false;
    $scope.showAddRoleModal = function(){
    	$scope.addRoleModal = true;

    }
    // new role object
    $scope.role = {};
    $scope.addRoleSubmit = function(){
         $http({
                method:"POST",
                url:"/api/roles",
                data:{
                    "role_name":$scope.role['name']
                }
            }).then(function successCallback(data) {
                $scope.Roles[data.data.added_role]=data.data.added_role_id;
            }, function errorCallback(response) {
                try {
                    $scope.Eror=response.data[0].validation_error;
                }
                catch (err) {
                    $scope.Eror=response.data.error;
                }
                $scope.customEror=true;
            })
    };
    $scope.deleteRole=function(id){
            $http({
                method:"DELETE",
                headers: {"Content-Type": "application/json;charset=utf-8"},
                url:"/api/roles",
                data:{
                    "role_id":id
                }
            }).then(function successCallback(data) {
                // delete role from local database
                for(r in $scope.Roles){
                    if($scope.Roles[r] == data.data['deleted_role']){
                        delete $scope.Roles[r]
                    }
                }
                if(data.data.error){
                $scope.Eror=data.data.error
                $scope.customEror=true
                }
                console.log(data)
            }, function errorCallback(response) {
                $scope.Eror=response
                $scope.customEror=true
            })
        }
        $scope.editRoleObj={}
        $scope.editRole=function(){
            $http({
                    method:"PUT",
                    url:"/api/roles",
                    data:{
                    "new_role_name":$scope.editRoleObj['name'],
                    "role_id" : $scope.editRoleObj['id']
                    }
                }).then(function successCallback(data) {

                },function errorCallback(response) {
                $scope.Eror=response
                $scope.customEror=true
            })
        }
    $scope.editRoleModal=false
    $scope.showEditRoleModal=function(name,id){
        $scope.editRoleObj = {
            'name':name,
            "id":id
        }
        $scope.editRoleModal=true
    }

    $scope.rolePerm=false

    $scope.selectPerm=function(ev,perm){
        // Define all permision,wich already bind
        if(ev.currentTarget.classList.contains("selected")){
            ev.currentTarget.classList.remove("selected")
            $scope.listToSend.splice( $scope.listToSend.indexOf(perm.permission_id), 1 )
            delete $scope.selectPermObj[perm.permission_id]     
        }
        else{
            ev.currentTarget.classList.add("selected")
            $scope.listToSend.push(perm.permission_id)
            $scope.selectPermObj[perm.permission_id]=perm

        }
}
    
    $scope.showRolePerm=function(name,id){
        $scope.rolePerm=true
        $scope.rolePermObj={
            "name":name,
            "id":id
        }

        $scope.selectPermObj={}
        $scope.listToSend=[]

        $http({
            method:"GET",
            url:"/api/role_permissions",
            params:{
                role_id:$scope.rolePermObj.id
            }
        }).then(function successCallback(data) {
                $scope.actualPermInRole = data.data.actual
                for(var i=0;i < $scope.actualPermInRole.length;i++){
                if($scope.listToSend.indexOf($scope.actualPermInRole[i].id) == -1){
                $scope.listToSend.push($scope.actualPermInRole[i].id)
                $scope.selectPermObj[$scope.actualPermInRole[i].id]=$scope.actualPermInRole[i]
            }
            
        }
            /* define function for ng-show atribute for permision.
                If listToSend contains it, ng-show return false
            */
            $scope.checkInActual=function(id){
                console.log($scope.listToSend)
                var list=[]
                     $scope.actualPermInRole.forEach(function(elem){
                        list.push(elem.id)
                     })
                if(list.indexOf(id) !=-1){
                    return false
                    }
                else return true
                }
            }, function errorCallback(response) {
                $scope.Eror=response
                $scope.customEror=true
            })

    }
    $scope.deletePermFormRole=function(perm){
         if($scope.actualPermInRole.length-1 !== 0){
            $scope.listToSend.splice( $scope.listToSend.indexOf(perm.id), 1 )
            $scope.actualPermInRole.forEach(function(elem,index){
            if(elem.id == perm.id){
                // delete perm
                $scope.actualPermInRole.length= $scope.actualPermInRole.length-1
                delete $scope.actualPermInRole[index]
               
            }
            console.log($scope.actualPermInRole.length)
         })
         console.log($scope.actualPermInRole)
         delete $scope.selectPermObj[perm.id]
         }
         else {
            $scope.Eror='at least one bind element'
            $scope.customEror=true
         }
    }
    // data for filter
    $scope.searchWord=""

    /*func for bind  permision to resource*/
    $scope.bindResPerm=function(){

        if($scope.actualPermInRole.length !== 0 ){
        $scope.listToSend=[]
        for(id in $scope.selectPermObj){
            $scope.listToSend.push(id)
        }
        console.log($scope.listToSend);
         $http({
            method:"PUT",
            url:"/api/role_permissions",
            data:{
                "role_id":$scope.rolePermObj.id, 
                "permission_id":$scope.listToSend
            }
            }).then(function successCallback(data) {
                console.log(data)
            }, function errorCallback(response) {
                console.log(response)
            })

            $scope.rolePerm=false
        }
        else {
            $scope.Eror='response'
            $scope.customEror=true
        }
        
    }

    $scope.showResPerm=function(id){
        $http({
            method:"GET",
            url:"/api/permissions",
            params:{
                resource_id:id
            }
        }).then(function successCallback(data) {

            }, function errorCallback(response) {
                $scope.Eror=response
                $scope.customEror=true
            })
    }
    //Users
    $scope.changeRole=function(user_obj){
        $scope.Roles.forEach(function (elem,index){
            if(elem == user_obj.id ){

            }
        })
        $http({
            method:"POST",
            url:"/api/user_roles",
            data:{
                "role_id":role_id,
                "user_id":user_id
            }
        }).then(function successCallback(data) {
                console.log(data)
            }, function errorCallback(response) {
                $scope.Eror=response
                $scope.customEror=true
            })
    }
}]);