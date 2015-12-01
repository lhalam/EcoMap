app.controller('detailedProblemCtrl', ['$scope','$rootScope', '$state', '$http', 'toaster',
    function($scope,$rootScope, $state, $http, toaster) {
        $scope.maxSeverity =[1,2,3,4,5]
        $http({
            "method":"GET",
            "url":"/api/problem_detailed_info/"+$state.params['id']
        }).then(function successCallback(data){
            $rootScope.selectProblem = data.data[0][0]
            console.log($rootScope.selectProblem)
            $rootScope.mapParams = {
                center: {
                  latitude:$rootScope.selectProblem['latitude'], 
                  longitude: $rootScope.selectProblem['longitude']
                },
                zoom: 17
              };
               console.log($rootScope.selectProblem)
        }, function errorCallback(error){})
       $scope.close=function(){
        $state.go('map')
       }
  
}]);