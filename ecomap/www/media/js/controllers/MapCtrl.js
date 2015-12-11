app.controller('MapCtrl', ['$scope', '$http', 'uiGmapGoogleMapApi','$rootScope','uiGmapIsReady',"$state",
  function($scope, $http, uiGmapGoogleMapApi,$rootScope, uiGmapIsReady,$state) {
    $scope.markers = [];
    console.log($rootScope.centerMap)
    if(!$rootScope.centerMap || !$rootScope.zoomMap){
      $rootScope.centerMap = {
        lat: 49.357826, 
        lng: 31.518239
      }
      $rootScope.zoomMap = 6;
    }

    $scope.initMap = function () {
      map = new google.maps.Map(document.getElementById('map'), {
        center:$rootScope.centerMap,
        zoom: $rootScope.zoomMap,
        options:{
          panControl    : true,
          zoomControl   : true,
          scaleControl  : true,
          mapTypeControl: true,

        }
     });
      $scope.loadProblems()
    }
    $scope.loadProblems = function() {
      $http({
        method: 'GET',
        url: '/api/problems'
      }).then(function successCallback(response) {
        angular.forEach(response.data,function(marker,key){
          var pos = {
            lat: marker.latitude,
            lng: marker.longitude
          };
          var new_marker =  new google.maps.Marker({
            position: pos,
            map: map,
            id:key,
            problem_type_Id: marker.problem_type_Id,
            problemStatus : marker.status,
            doCluster:true,
            date:marker.date,
            icon : "/image/markers/" + marker.problem_type_Id + ".png",

          })
          new_marker.addListener('click', function() {
           var problem_id = this.problem_type_Id;
           console.log(problem_id)
           $state.go("detailedProblem",{
            'id':problem_id
          });
         });
          $scope.markers.push(new_marker)
          new_marker.setMap(map);
        },
        function errorCallback(){

        })
      })
    }

    $scope.initMap()
//      if(!$scope.mapParams){
//        $rootScope.mapParams = {
//           center: {
//             latitude: 49.357826, 
//             longitude: 31.518239
//         },
//         zoom: 6
//     };
// }

// $scope.getMapParams = function() {
//     return $scope.mapParams;
// };

// $scope.zoomMarker = function(data) {
//     console.log(data)
//     $state.go("detailedProblem",{
//       'id':data.problem_id
//   });
//     console.log(data);
//     $scope.mapParams = {
//       center: {
//         latitude: data.latitude,
//         longitude: data.longitude
//     },
//     zoom: 17
// }
// };

// $scope.markers = [];
// $scope.loadProblems = function() {
//     $http({
//       method: 'GET',
//       url: '/api/problems'
//   }).then(function successCallback(response) {
//    uiGmapIsReady.promise(1).then(function(instances) {
//       instances.forEach(function(inst) {
//         var map = inst.map;
//         var uuid = map.uiGmap_id;
//         var mapInstanceNumber = inst.instance;
//         uiGmapIsReady.promise()
//         .then(function(instances) {
//           var maps = instances[0].map;
//           console.log(maps)
//           google.maps.event.trigger(maps, 'resize');
//           angular.forEach(response.data,function(marker,key){

//             var pos = {
//                 lat: marker.latitude,
//                 lng: marker.longitude
//             };

//             var new_marker =  new google.maps.Marker({
//               position: pos,
//               map: maps,
//               id:key,
//               problem_type_Id: marker.problem_type_Id,
//               problemStatus : marker.status,
//               icon : "/image/markers/" + marker.problem_type_Id + ".png",


//           })
//             window.google.maps.event.addListener(new_marker, 'click', function () {
//               console.log(this)
//               $scope.zoomMarker(marker)
//           });

//              $scope.markers.push(new_marker);
//              console.log($scope.markers);

//             //$scope.markers[key].iconUrl = "/image/markers/" + marker.problem_type_Id + ".png";
//         })
//           console.log("Out of forEach");
//       });
// });
//           console.log("Out of gmap");

// });

// }, function errorCallback(error) {});
// };

// $scope.loadProblems();
//           console.log("after problem loading");

// uiGmapIsReady.promise()
// .then(function(instances) {
//   var maps = instances[0].map;
//   google.maps.event.trigger(maps, 'resize');
// });
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


  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
  };

  $scope.toggleMin = function() {
    $scope.minDate = $scope.minDate ? null : new Date();
  };
  $scope.toggleMin();
  $scope.maxDate = new Date(2020, 5, 22);

  $scope.open = function($event) {
    $scope.status.opened = true;
  };

  $scope.setDate = function(year, month, day) {
    $scope.dt = new Date(year, month, day);
  };

  $scope.dateOptions = {
    formatYear: 'yy',
    startingDay: 1
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];

  $scope.status = {
    opened: false
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 2);
  $scope.events =
  [
  {
    date: tomorrow,
    status: 'full'
  },
  {
    date: afterTomorrow,
    status: 'partially'
  }
  ];

  $scope.getDayClass = function(date, mode) {
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i=0;i<$scope.events.length;i++){
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  };

}]);
