app.controller('MapCtrl', ['$scope', '$http', '$rootScope',"$state", 'MapFactory',
  function($scope, $http, $rootScope, $state, MapFactory) {
    $scope.markers = [];
    // console.log('$rootScope.centerMap')
    // if(!$rootScope.centerMap || !$rootScope.zoomMap){
    //   $rootScope.centerMap = {
    //     lat: 49.357826, 
    //     lng: 31.518239
    //   }
    //   $rootScope.zoomMap = 6;
    // }

    // $scope.initMap = function () {
    //   $rootScope.map = new google.maps.Map(document.getElementById('map'), {
    //     center:$rootScope.centerMap,
    //     zoom: $rootScope.zoomMap,
    //     options:{
    //       panControl    : true,
    //       zoomControl   : true,
    //       scaleControl  : true,
    //       mapTypeControl: true,

    //     }
    //  });
    //   google.maps.event.addListenerOnce($rootScope.map, 'idle', function() {
    //     console.log("Resizing map...");
    //     google.maps.event.trigger($rootScope.map, 'resize');
    //   });
      
    //   $scope.loadProblems()
    // }


    // $scope.loadProblems = function() {
    //   $http({
    //     method: 'GET',
    //     url: '/api/problems'
    //   }).then(function successCallback(response) {
    //     angular.forEach(response.data,function(marker,key){
    //       var pos = {
    //         lat: marker.latitude,
    //         lng: marker.longitude
    //       };
    //       var new_marker =  new google.maps.Marker({
    //         position: pos,
    //         map: MapFactory.getInst(),
    //         id:marker.problem_id,
    //         problem_type_Id: marker.problem_type_Id,
    //         problemStatus : marker.status,
    //         doCluster:true,
    //         date:marker.date,
    //         icon : "/image/markers/" + marker.problem_type_Id + ".png",

    //       })
    //       new_marker.addListener('click', function() {
    //        var problem_id = this['id'];
    //        console.log(problem_id)
    //        $state.go("detailedProblem",{
    //         'id':problem_id
    //       });
    //      });
    //       $scope.markers.push(new_marker)
    //       new_marker.setMap(MapFactory.getInst());
    //     },
    //     function errorCallback(){

    //     })
    //   })
    // }
    MapFactory.initMap({lat: 54.468077, lng:30.521018}, 6);
    MapFactory.turnResizeOn();
    $scope.markers = MapFactory.loadProblems();
    // $scope.loadProblems();

    // $scope.initMap()
    // FILTER
    $("#filerToogle").click(function(){
      console.log("clic")
      $("#filterProb").toggleClass( "showFilter" );
    })
    $scope.Types = {
      '1': 'Проблеми лісів',
      '2': 'Сміттєзвалища',
      '3': 'Незаконна забудова',
      '4': 'Проблеми водойм',
      '5': 'Загрози біорізноманіттю',
      '6': 'Браконьєрство',
      '7': 'Інші проблеми'
    }
    $scope.Status = {
      "Unsolved":"Нова",
      "Resolved":"Вирішена"
    }
    $scope.selectedType = [];
    $scope.selectedStatus = [];

    for(type in $scope.Types){
     $scope.selectedType.push(type)
   }
   for(s in $scope.Status){
    $scope.selectedStatus.push(s)
  }
  console.log($scope.selectedStatus)
  $scope.toggleType = function(type_id){

    if($scope.selectedType.indexOf(type_id+"")!== -1){
      $scope.selectedType.splice($scope.selectedType.indexOf(type_id),1)  

    }
    else{
      console.log("else")
      $scope.selectedType.push(type_id)
    }

    $scope.filterMarker()
  }
  $scope.toggleStatus = function(status){
    console.log($scope.selectedStatus)
    if($scope.selectedStatus.indexOf(status)!== -1){
      $scope.selectedStatus.splice($scope.selectedStatus.indexOf(status),1)  
    }
    else{
      $scope.selectedStatus.push(status)
    }


    $scope.filterMarker()
  }
  $scope.selectTime = function(marker){
    if(!$scope.dt){
      return false
    }
    else if(marker.date > $scope.dt.from.getTime()/1000 && marker.date < $scope.dt.to.getTime()/1000){
      console.log(marker.date > $scope.dt.from.getTime()/1000 && marker.date < $scope.dt.to.getTime()/1000)
      return false
    }
    else return true
  }
  $scope.filterMarker = function(){
   angular.forEach($scope.markers, function(marker, key){   
    if($scope.selectedType.indexOf(marker.problem_type_Id+"") === -1 ||
      $scope.selectedStatus.indexOf(marker['problemStatus']) === -1 || 
      $scope.selectTime(marker)
      ){ 

      marker.setVisible(false);

  } else{
    marker.setVisible(true);
  }
})
 }



}]);
