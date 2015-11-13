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
            //console.log($scope.Resources)

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
            if(data.data['deleted_resource']){
                deletedResId=data.data['deleted_resource']
                for (name in $scope.Resources){
                if ($scope.Resources[name] === id){
                    console.log($scope.Resources[name])
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
            $scope.addResModal=false
            $scope.Eror=response.statusText
            $scope.customEror=true
        });
    };


    //permission section
    $scope.addPermModal = false;
    $scope.showAddPermModal = function(){
    	$scope.addPermModal = true;
    };
    $scope.show=function(){
        console.log($scope.editPerm)
    }
    $scope.perm = {};
    $scope.addPermSubmit = function(){
        $http({
            method:"POST",
            headers: {"Content-Type": "application/json;charset=utf-8"},
            url:"/api/permissions",
            data:{
            "resource_id":4,
            "action": 'GET',
            "modifier": 'Own',
            "description": 'Got some new'
            } 
        }).then(function successCallback(data) {
         console.log(data)
        }, function errorCallback(response) {
            console.log(perm)
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
                if(data.data['deleted_resource']){
                    deletedResId=data.data['deleted_permission:']
                    for (name in $scope.Permisions){
                        console.log(name)
                    if ($scope.Permisions[name] === perm.permission_id){
                        //console.log($scope.Resources[name])
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
    }

    // Role section
    $scope.addRoleModal = false;
    $scope.showAddRoleModal = function(){
    	$scope.addRoleModal = true;

    }

    $scope.role = {};
    $scope.addRoleSubmit = function(){

    };

}]);