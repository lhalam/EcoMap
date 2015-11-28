app.controller('MapCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.mapParams = { center: { latitude: 49, longitude: 30 }, zoom: 6 };
    $scope.getMapParams = function(){
        return $scope.mapParams;
    };    

    // $scope.positions =[
    //   {id: 1, pos:{'latitude': 48.71, 'longitude': 31.22}},
    //   {id: 2, pos:{'latitude': 49.72, 'longitude': 33.20}},
    //   {id: 3, pos:{'latitude': 49.50, 'longitude': 28.19}},
    //   {id: 4, pos:{'latitude': 49.46, 'longitude': 29.18}},
    //   {id: 5, pos:{'latitude': 49.97, 'longitude': 32.17}},
    //   {id: 6, pos:{'latitude': 50.76, 'longitude': 31.16}},
    //   {id: 7, pos:{'latitude': 49.17, 'longitude': 33.15}}
    // ];

    $scope.zoomMarker = function(data){
        console.log(data);
        $scope.mapParams = { 
            center: { latitude: data.model.latitude,
                      longitude: data.model.longitude },
            zoom: 17
        }
    };

    $scope.markers = [];
    $scope.loadProblems = function(){
        $http({
            method: 'GET',
            url: '/api/problems'
        }).then(function successCallback(response){
            $scope.markers = response.data;
            console.log($scope.markers);
        }, function errorCallback(error){});
    }
    $scope.loadProblems();

}])
