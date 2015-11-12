app.controller('AdminCtrl', ['$scope', function($scope){
    $scope.addResModal = false;
    $scope.triggerAddResModal = function(){
        $scope.addResModal = true;
    };
}]);