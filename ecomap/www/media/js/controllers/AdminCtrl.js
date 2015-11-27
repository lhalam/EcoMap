app.controller('AdminCtrl', ['$scope','$http', 'toaster', function($scope,$http, toaster){

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
    $scope.selectCountObj={
        "1":'5',
        "2":"10",
        "3":"15"
    }
    $scope.selectCount={
        'selected':"5"
    }

    $scope.msg = {
        editSuccess: function(msg){
            toaster.pop('success', 'Редагування', 'Редагування ' + msg + ' здійснено успішно!');
        },
        deleteSuccess: function(msg){
            toaster.pop('success', 'Видалення', 'Видалення ' + msg + ' здійснено успішно!');
        },
        createSuccess: function(msg){
            toaster.pop('success', 'Додавання', 'Додавання ' + msg + ' здійснено успішно!');
        },
        editError: function(msg){
            toaster.pop('error', 'Редагування', 'При редагуванні ' + msg + ' виникла помилка!');
        },
        deleteError: function(msg){
            toaster.pop('error', 'Видалення', 'При видаленні ' + msg + ' виникла помилка!');
        },
        createError: function(msg){
            toaster.pop('error', 'Додавання', 'При додаванні ' + msg + ' виникла помилка!');
        },
    };
    $scope.loadRes=function(){
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.Resources = data.data

        }, function errorCallback(response) {
            //console.log(response)
        });
    }
    $scope.loadPerm=function(){
        $http({
                method: "GET",
                url: '/api/all_permissions',
               
            }).then(function successCallback(data) {
                $scope.Permisions=data.data;
                //console.log($scope.Permisions)
                
            }, function errorCallback(response) {
                //console.log(response)
            })

    }
    $scope.loadRole=function(){
         $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
                //console.log($scope.Roles)
            },function errorCallback(response) {
                //console.log(response)
            })

    }

    $scope.loadData=function(){

        //load resources
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.Resources = data.data

        }, function errorCallback(response) {
            //console.log(response)
        });

        //load permisions
         $http({
                method: "GET",
                url: '/api/all_permissions',
               
            }).then(function successCallback(data) {
                $scope.Permisions=data.data;
                //console.log($scope.Permisions)
                
            }, function errorCallback(response) {
                //console.log(response)
            })

        // load roles

        $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
                //console.log($scope.Roles)
            },function errorCallback(response) {
                //console.log(response)
            })

        $http({
            method:'GET',
            url:"/api/user_roles"
        }).then(function successCallback(data) {
                //$scope.Roles=data.
                $scope.Users=data.data
                //console.log("user_roles")

            },function errorCallback(response) {
                //console.log(response)
            })

    }

    $scope.loadData()

	// resource section

    //trigers for modal windows
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
        $scope.newResource = {};
    };

     $scope.addResource = function(){
         
         console.log($scope.newResource)
         $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': $scope.newResource.name
            }
        }).then(function successCallback(data) {
        $scope.loadRes()
        $scope.addResModal=false
        $scope.msg.createSuccess('ресурсу');
        }, function errorCallback(response) {
            $scope.addResModal=false
            $scope.msg.createError('ресурсу');
        });

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
        console.log($scope.editResObj)
        $http({
        method:"PUT",
        url:"/api/resources",
        data:{
          "resource_name":$scope.editResObj['name'],
          "resource_id" : $scope.editResObj['id']
        }
        }).then(function successCallback(data) {
            $scope.loadRes()
            $scope.editResModal = false;
            $scope.msg.editSuccess('ресурсу');
        }, function errorCallback(response) {
            //console.log("response")
            $scope.msg.editError('ресурсу');
            //$scope.addResModal=false
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
            $scope.loadRes()
            $scope.msg.deleteSuccess('ресурсу');
        }, function errorCallback(response) {
            $scope.msg.deleteError('ресурсу');
        })
   	};

    //Create new resource object 

   

    //permission section

    //Permision modal windows trigers
    $scope.addPermModal = false;
    $scope.showAddPermModal = function(){
    	$scope.addPermModal = true;
        $scope.perm = {};
    };
    $scope.show=function(){
       var name= $scope.perm.resource_name
    }
    // create obj for new permision
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
            $scope.loadPerm()
            $scope.addPermModal = false;
            $scope.msg.createSuccess('права');
        }, function errorCallback(response) {
            $scope.msg.createError('права');
            //$scope.Eror=response.statusText
            //$scope.customEror=true
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
                "action":$scope.editPerm['action'],
                "modifier":$scope.editPerm.modifier, 
                "description":$scope.editPerm['description']
            }
        }).then(function successCallback(data) {
                console.log(data)
                $scope.editPermModal = false;
                $scope.msg.editSuccess('права');
                $scope.loadPerm()

            }, function errorCallback(response) {
                $scope.msg.editError('права');
                //console.log(response)
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
             console.log(data)
           }
           else{
                $scope.msg.deleteError('права');
           }
            
            console.log(data)
            }, function errorCallback(response) {
                 $scope.msg.deleteError('права');
        })
    }

    // Role section

    $scope.addRoleModal = false;
    $scope.showAddRoleModal = function(){
    	$scope.addRoleModal = true;
        $scope.role = {};

    }
    // new role object
    

    $scope.addRoleSubmit = function(){
        console.log($scope.role['name'])
         $http({
                method:"POST",
                url:"/api/roles",
                data:{
                    "role_name":$scope.role['name']
                }
            }).then(function successCallback(data) {
                $scope.msg.createSuccess('ролі');
                $scope.Roles[data.data.added_role]=data.data.added_role_id;
                $scope.addRoleModal = false;
            }, function errorCallback(response) {
                $scope.msg.createError('ролі');
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
                        $scope.msg.deleteSuccess('ролі');
                    }
                }
                if(data.data.error){
                $scope.msg.deleteError('ролі');
                }
               
            }, function errorCallback(response) {
                $scope.msg.deleteError('ролі');
            })
        }
        $scope.editRoleObj={}
        $scope.editRole=function(){
            //console.log()
            $http({
                    method:"PUT",
                    url:"/api/roles",
                    data:{
                    "role_name":$scope.editRoleObj['name'],
                    "role_id" : $scope.editRoleObj['id']
                    }
                }).then(function successCallback(data) {
                $scope.loadRole()
                $scope.msg.editSuccess('ролі');
                $scope.editRoleModal=false
                },function errorCallback(response) {
                //$scope.Eror=response
                //$scope.customEror=true
                $scope.msg.editError('ролі');
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
        $scope.actualPermInRole.push(perm)
        $scope.listToSend.push(perm.permission_id)
        // Define all permision,wich already bind
       
        
        console.log($scope.actualPermInRole)
        console.log(perm)
        
}
    $scope.isChecked=function(perm){
       if($scope.listToSend){
         if($scope.listToSend.indexOf(perm.permission_id) !== -1){
                return true
        }
       }


    }

    $scope.backToRole=function(){
        $scope.rolePermTable = true
        $scope.rolePermBlock = false
    }
    $scope.rolePermTable = true
    $scope.rolePermBlock = false
    $scope.showRolePerm=function(name,id){
        $scope.rolePermTable = false
        $scope.rolePermBlock = true
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
                console.log(data)
                $scope.actualPermInRole = data.data.actual
                for(var i=0;i < $scope.actualPermInRole.length;i++){
                if($scope.listToSend.indexOf($scope.actualPermInRole[i].id) === -1){
                $scope.listToSend.push($scope.actualPermInRole[i].id)
                $scope.selectPermObj[$scope.actualPermInRole[i].id]=$scope.actualPermInRole[i]
               
            }
            
        }
            /* define function for ng-show atribute for permision.
                If listToSend contains it, ng-show return false
            */
            $scope.checkInActual=function(id){
                ////console.log($scope.listToSend)
                $scope.actualPermList=[]
                     $scope.actualPermInRole.forEach(function(elem){
                        if(elem.id === id){
                            return true
                            console.log(id)
                        }
                        else return false
                        //$scope.actualPermList.push(elem.id)
                     })
                
                }
            }, function errorCallback(response) {
                $scope.msg.deleteError('ролі');
            })

    }


    $scope.deletePermFormRole=function(perm){
            $scope.listToSend.splice( $scope.listToSend.indexOf(perm.id), 1 )
            $scope.actualPermInRole.forEach(function(actual_perm){
                if(actual_perm.permission_id === permission_id){
                    $scope.actualPermInRole.splice( $scope.actualPermInRole.indexOf(perm.permission_id), 1 )
                }
            })
            console.log(perm)
          
        
    }
    // data for filter
    $scope.searchWord=""

    /*func for bind  permision to resource*/
    $scope.bindResPerm=function(){

        $scope.listToSend=[]
        for(id in $scope.selectPermObj){
            $scope.listToSend.push(id)
        }
        //console.log($scope.listToSend);
         $http({
            method:"PUT",
            url:"/api/role_permissions",
            data:{
                "role_id":$scope.rolePermObj.id, 
                "permission_id":$scope.listToSend
            }
            }).then(function successCallback(data) {



                //$scope.actualPermInRole.push()
                //console.log($scope.actualPermInRole)
                $scope.msg.editSuccess('прав');
                 $scope.rolePermTable = true
                $scope.rolePermBlock = false
            }, function errorCallback(response) {
                $scope.msg.editError('прав');
            })


        
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
                
                
            })
    }

    //Users
    $scope.changeRole=function(user_obj){
        console.log(user_obj)
        var role_id;
        for (role in $scope.role_obj){
            if($scope.role_obj[role] == user_obj.role_name){
                //console.log($scope.role_obj[role] )
                role_id = role
            }
        }
        $http({
            method:"POST",
            url:"/api/user_roles",
            data:{
                "role_id":role_id,
                "user_id":user_obj.id
            }
        }).then(function successCallback(data) {
                $scope.msg.editSuccess('користувача');
            }, function errorCallback(response) {
                //$scope.Eror=response
                //$scope.customEror=true
                $scope.msg.editError('користувача');
            })
    }
   // Pagination
   $scope.loadPagination=function(){

    $http({
        method:"GET",
        url:"/api/user_page",
        params:{
            per_page:4,
            offset:0,
        }
    }).then(function successCallback(data) {
                console.log(data)
            }, function errorCallback(response) {
                //$scope.Eror=response
                //$scope.customEror=true
                $scope.msg.editError('користувача');
    })


  $scope.totalItems = 62;
  $scope.currentPage = 3;
  $scope.fromPage = 1;
  $scope.bigCurrentPage = 1;
  $scope.bigTotalItems = $scope.Users.length / $scope.selectCount['selected']*10;
  if($scope.bigCurrentPage === 1){
    $http({
        method:"GET",
        url:"/api/user_page",
        params:{
            per_page:$scope.selectCount['selected'],
            offset:0,
        }
        }).then(function successCallback(data) {
            $scope.selectedUsers = data.data
                console.log(data)
            }, function errorCallback(response) {
                //$scope.Eror=response
                //$scope.customEror=true
                $scope.msg.editError('користувача');
    })
  }


  $scope.$watch('bigCurrentPage', function(newValue, oldValue) {

    $scope.bigTotalItems = $scope.Users.length / $scope.selectCount['selected']*10;
    var stepCount =$scope.selectCount['selected']
    console.log("new :"+$scope.selectCount['selected']*newValue)
    console.log($scope.selectCount['selected']*newValue - stepCount)
        $http({
        method:"GET",
        url:"/api/user_page",
        params:{
            per_page:$scope.selectCount['selected'],
            offset:$scope.selectCount['selected']*newValue -stepCount,
        }
        }).then(function successCallback(data) {
            $scope.selectedUsers = data.data
                console.log(data)
            }, function errorCallback(response) {
                //$scope.Eror=response
                //$scope.customEror=true
                $scope.msg.editError('користувача');
    })
    });
   $scope.change=function(currPage){
        $scope.bigCurrentPage = currPage


    }

  $scope.maxSize = 6;

  console.log($scope.bigTotalItems)
   }


}]);