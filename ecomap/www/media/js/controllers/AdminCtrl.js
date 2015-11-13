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
        console.log("load")
        $http({
            method: 'GET',
            url: '/api/resources'
        }).then(function successCallback(data) {
            $scope.Resources = data.data
            console.log($scope.Resources)

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
            $scope.Resources=data.data
        }, function errorCallback(response) {
            console.log(response)
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
        }, function errorCallback(response) {
            console.log(response)
        })
   	};

    $scope.new_res = {};
    var data = {
        'resource_name': $scope.new_res['name']

    }
    $scope.addResource = function(){
         $http({
            method: "POST",
            url: "/api/resources",
            data:{
                'resource_name': $scope.new_res['name']
            }
        }).then(function successCallback(data) {
            console.log(data.data)
        }, function errorCallback(response) {
            console.log(response)
        });
    };


    //permission section
    $scope.addPermModal = false;
    $scope.showAddPermModal = function(){
    	$scope.addPermModal = true;
    };

    $scope.perm = {};
    $scope.addPermSubmit = function(){

    };

    $scope.editPermModal = false;
    $scope.showEditPermModal = function(){
    	$scope.editPermModal = true;
    }
    // function for editPerm submit
    $scope.editPermSubmit = function(id){

    };


    // Role section
    $scope.addRoleModal = false;
    $scope.showAddRoleModal = function(){
    	$scope.addRoleModal = true;
    }

    $scope.role = {};
    $scope.addRoleSubmit = function(){

    };

}]);