var app=angular.module('app',['ui.bootstrap', 'ngCookies']);
//
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

// app.controller("UserController",function ($scope, $http, $rootScope, $window){

//   $scope.user = {};
//     $scope.singinUser = function() {
//         $http({
//             method : 'POST',
//             url : '/api/login',
//             data : $scope.user
//         })
//         .then(function successCallback(data) {
//           $rootScope.userObj=data.data;
//           $(".message").addClass("active");
//           $("#message_head").text("Welcome");
//           $("#message_text").text("sing in was completed")
//           $('[showform]').each(function(num,elem) {
//             if(elem.getAttribute("showform") =="True"){
//               elem.style="diplay:block"
//             }
//             else{
//                elem.style="diplay:none"
//             }
//           });         
//         },
//         function errorCallback(data) {
//           $(".message").addClass("active");
//           $("#message_head").text("Sorry");
//           $("#message_text").text(data.data.status || "Error")
          
//         })
// }
// })
// app.controller("RegistrCtrl",function ($scope, $http,$rootScope){
//   $scope.newUser = {};
//     $scope.singupUser = function() {
//       console.log($scope.newUser)
//         $http({
//             method : 'POST',
//             url : '/api/register',
//             data : $scope.newUser
//         })
//         .then(function successCallback(data) {
//           $rootScope.userObj=data.data;
//           $(".message").addClass("active");
//           $("#message_head").text("Welcome");
//           $("#message_text").text("registration was completed")
          
//         },
//         function errorCallback(data) {
//           $(".message").addClass("active");
//           $("#message_head").text("Sorry");
//           $("#message_text").text(data.data.status || "Something was wrong")
//         })
// }
// })
// app.controller("logOutUser",function ($scope,$window,$rootScope){
//   $scope.logOut=function (){
//     $rootScope.userObj= undefined
//     $window.location="/logout"
//      /*logout*/
//   }
// })

app.controller('LoginCtrl', ['$scope',  '$cookies', '$http', '$rootScope', function($scope, $cookies, $http, $rootScope){

  $scope.showLoginModal = false;
  $scope.toggleLoginModal = function(){
    $scope.showLoginModal = !$scope.showLoginModal;
  };

  $scope.showRegisterModal = false;
  $scope.toggleRegisterModal = function(){
    $scope.showRegisterModal = !$scope.showRegisterModal;
  };  

  // $scope.registerError = "";
  // $scope.loginError = "";
  // $scope.setError = function(error){
  //   $scope.registerError = error;
  // }
  // $scope.setLoginError = function(error){
  //   $scope.loginError = error;
  // }

  $scope.checkLogined = function(){
    if($cookies.get('name') && $cookies.get('surname')){
      return $cookies.get('name') + " " + $cookies.get('surname');
    } else{
      return null;
    }
  }

  $scope.newUser = {};
  $scope.checkIfExists = function(){
    console.log($scope.newUser);
    $http({
      method: 'POST',
      url: '/api/email_exist',
      data: $scope.newUser
    }).then(function successCallback(responce){
      var form = angular.element("#emailDiv");
      form.addClass("has-error");
      var error = angular.element("#existError");
      error.removeClass("hidden");
    },
    function errorCallback(responce){
      var form = angular.element("#emailDiv");
      form.removeClass("has-error");
      var error = angular.element("#existError");
      error.addClass("hidden");
      console.log("herer");
    });
  };

  $scope.Register = function(){
    if(!$scope.newUser.email || !$scope.newUser.firstName ||
      !$scope.newUser.lastName || !$scope.newUser.password ||
      !$scope.newUser.pass_confirm){
      return null;
    }
    if($scope.newUser.password == $scope.newUser.pass_confirm){
      $http({
        method: 'POST',
        url: '/api/register',
        data: $scope.newUser
      }).then(function successCallback(responce){
        $scope.showRegisterModal = false;
        console.log(responce.data);
        $scope.user.email = $scope.newUser.email;
        $scope.user.password = $scope.newUser.password;
        $scope.Login();
        $scope.newUser = {};
      },
        function errorCallback(responce){
          // if(responce.status == 400){
          //   var form = angular.element("#emailDiv");
          //   form.addClass("has-error");
          //   var error = angular.element("#emailError");
          //   error.text = "Ця електронна пошта вже зареєстрована!";
          //   $scope.existingEmail = newUser.email;
          // }
        });
    }
  };

  $scope.user = {};
  $scope.Login = function(){
    if(!$scope.user.email || !$scope.user.password){
      return null;
    }
    $http({
      method: 'POST',
      url: '/api/login',
      data: $scope.user
    }).then(function successCallback(responce){
      $scope.showLoginModal = false;
      $cookies.put('name', responce.data.name);
      $cookies.put('surname', responce.data.surname);
      $cookies.put('id', responce.data.id);
      $scope.user = {};
      console.log(responce);
    },
      function errorCallback(data){
      });
  };

  $scope.Logout = function(){
    $http({
      method: 'POST',
      url: '/api/logout',
      data: $scope.user
    }).then(function successCallback(responce){
      $cookies.remove('name');
      $cookies.remove('surname');
      $cookies.remove('id');
    },
      function errorCallback(data){});
  };

}]);

app.directive('modal', function () {
    return {
      template: '<div class="modal fade">' + 
          '<div class="modal-dialog">' + 
            '<div class="modal-content">' + 
              '<div class="modal-header">' + 
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' + 
                '<h4 class="modal-title">{{ title }}</h4>' + 
              '</div>' + 
              '<div class="modal-body" ng-transclude></div>' + 
            '</div>' + 
          '</div>' + 
        '</div>',
      restrict: 'E',
      transclude: true,
      replace:true,
      scope:true,
      link: function postLink(scope, element, attrs) {
        scope.title = attrs.title;

        scope.$watch(attrs.visible, function(value){
          if(value == true)
            $(element).modal('show');
          else
            $(element).modal('hide');
        });

        $(element).on('shown.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = true;
          });
        });

        $(element).on('hidden.bs.modal', function(){
          scope.$apply(function(){
            scope.$parent[attrs.visible] = false;
          });
        });
      }
    };
});
