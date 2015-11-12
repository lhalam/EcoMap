app.controller('AdminCtrl', ['$scope', function($scope){

	// here you fetch all resources, permission, roles from backend


	// resource section
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
    };

    $scope.editResModal = false;
    $scope.showEditResModal = function(id){
    	$scope.editResObj={
    		'id':id
    	};
    	$scope.editResModal = true;
    }
    $scope.res = {};
    $scope.editResource = function(){

    	//...
    };

   	$scope.deleteResource = function(id){

   	};

    $scope.new_res = {};
    $scope.addResource = function(){

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