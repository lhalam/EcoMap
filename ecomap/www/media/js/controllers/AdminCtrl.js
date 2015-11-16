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
                //console.log($scope.Permisions)
                
            }, function errorCallback(response) {
                console.log(response)
            })

        // load roles

        $http({
                method:"GET",
                url:"/api/roles",

            }).then(function successCallback(data) {
                $scope.Roles=data.data
                //console.log($scope.Roles)
            },function errorCallback(response) {
                console.log(response)
            })

    }

    $scope.loadData()

	// resource section
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
    };

    $scope.editResModal = false;
    $scope.showEditResModal = function(name,id){
    	$scope.editResObj={
            'name':name,
    		'id':id
    	};
    	$scope.editResModal = true;
    }
    $scope.res = {};
    $scope.editResource = function(){
        $http({
        method:"PUT",
        url:"/api/resources",
        data:{
          "new_resource_name":$scope.editResObj['name'],
          "resource_id" : $scope.editResObj['id']
        }
        }).then(function successCallback(data) {
            console.log(data)
        }, function errorCallback(response) {
            $scope.addResModal=false
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
            console.log(data)
            if(data.data['deleted_resource']){
                deletedResId=data.data['deleted_resource']
                for (name in $scope.Resources){
                if ($scope.Resources[name] === deletedResId){
                    delete $scope.Resources[name]
                }

                }
            }
            else {
                    console.log(data)
                    $scope.Eror=data.data['error']
                    $scope.customEror=true
                }        
        }, function errorCallback(response) {
            console.log(response)
            $scope.Eror=response.statusText
            $scope.customEror=true
        })
   	};

    $scope.new_res = {};
    $scope.addResource = function(){
         $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': $scope.new_res.name
            }
        }).then(function successCallback(data) {
        $scope.Resources[data.data.added_resource]=data.data.resource_id
        $scope.addResModal=false
         console.log(data)
        }, function errorCallback(response) {
            console.log(response)
            $scope.addResModal=false
            $scope.Eror=response.data.error
            $scope.customEror=true
        });
    };


    //permission section
    $scope.addPermModal = false;
    $scope.showAddPermModal = function(){
    	$scope.addPermModal = true;
    };
    $scope.show=function(){
       var name= $scope.perm.resource_name
        console.log($scope.OBJ)
    }
    $scope.perm = {};
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
            //$scope.Eror=data.data
            //$scope.customEror=true
        }, function errorCallback(response) {
            $scope.Eror=response.statusText
            $scope.customEror=true
        });
    };

    $scope.editPermModal = false;
    $scope.showEditPermModal = function(perm){
        console.log(perm)
        $scope.editPerm=perm
    	$scope.editPermModal = true;
    }
    // function for editPerm submit
    
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
                console.log(data.data)
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
            //console.log(data)
            
                if(data.data.deleted_permission){
                    //console.log(data.data['deleted_resource'])
                    deletedResId=data.data['deleted_permission']
                    for (name in $scope.Permisions){
                        console.log(name)
                        //console.log($scope.Permisions[name]['permission_id'])
                    if ($scope.Permisions[name]['permission_id'] === perm.permission_id){
                        console.log($scope.Permisions)
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

    $scope.role = {};
    $scope.addRoleSubmit = function(){
         $http({
                method:"POST",
                url:"/api/roles",
                data:{
                    "role_name":$scope.role['name']
                }
            }).then(function successCallback(data) {
                $scope.Roles[data.data.added_role]=data.data.added_role_id
                console.log($scope.Roles)
            }, function errorCallback(response) {
                console.log(response)
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
                for(r in $scope.Roles){
                    if($scope.Roles[r] == data.data['deleted_role']){
                        delete $scope.Roles[r]
                    }
                }
                if(data.data.error){
                $scope.Eror=data.data.error
                $scope.customEror=true
                }
                //$scope.Roles=data.data
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
                
                console.log(data)
            }, function errorCallback(response) {
                console.log(response)
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
    $scope.selectPermObj={}
    $scope.selectPerm=function(perm){
    $('#tablePermRole tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

        $scope.selectPermObj[perm.permission_id]=perm
        //console.log($scope.selectPermObj)
    }
    $scope.showRolePerm=function(name,id){

        $scope.rolePerm=true
        $scope.rolePermObj={
            "name":name,
            "id":id
        }
     
        
    }
    $scope.bindResPerm=function(){
        console.log($scope.Permisions)
        var listToSend=[]
        for(id in $scope.selectPermObj){
            listToSend.push(id)
        }
        console.log(listToSend)
         $http({
            method:"GET",
            url:"/api/permissions",
            params:{
                "role_id":$scope.rolePermObj.id, 
                "permission_id":listToSend
            }
            }).then(function successCallback(data) {
                //$scope.rolePermList=data.data
                console.log(data)
            }, function errorCallback(response) {
                console.log(response)
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

                console.log(data)
            }, function errorCallback(response) {
                console.log(response)
            })
    }
    $scope.example1model = [];
     $scope.example1data = [ {id: 1, label: "David"},
      {id: 2, label: "Jhon"},
       {id: 3, label: "Danny"}];
}]);