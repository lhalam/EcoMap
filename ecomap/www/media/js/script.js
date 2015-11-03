var app=angular.module('app',['ui.bootstrap'])
app.controller('DatepickerDemoCtrl', function ($scope) {
  $scope.today = function() {
    $scope.dt = new Date();
  };
  $scope.today();

  $scope.clear = function () {
    $scope.dt = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
  };

  $scope.toggleMin = function() {
    $scope.minDate = $scope.minDate ? null : new Date();
  };


  $scope.open = function($event) {
    $scope.status.opened1 = true;
  };
  $scope.open2 = function($event) {
    $scope.status.opened2 = true;
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
});
app.controller("UserController",function ($scope, $http,$rootScope,$window){
  $scope.user = {};
    $scope.singinUser = function() {

        $http({
            method : 'POST',
            url : '/login',
            data : $scope.user
        })
        .then(function successCallback(data) {
          $rootScope.userObj=data.data;
          console.log( $rootScope.userObj)
          
        },
        function errorCallback(data) {
          alert("sorry "+data.data.headers)
        })
        

}
})
app.controller("RegistrCtrl",function ($scope, $http,$rootScope){
  $scope.newUser = {};
    $scope.singupUser = function() {
      console.log($scope.newUser)
        $http({
            method : 'POST',
            url : '/register',
            data : $scope.newUser
        })
        .then(function successCallback(data) {
          $rootScope.userObj=data.data;
          console.log( $rootScope.userObj)
          
        },
        function errorCallback(data) {
          alert("sorry "+data.data.headers)
        })
}
});
app.controller("logOutUser",function ($scope,$window,$rootScope){
  $scope.logOut=function (){

    $rootScope.userObj= undefined;
    $window.location="/logout" /*logout*/
  }
});