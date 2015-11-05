var app=angular.module('app',['ui.bootstrap']);
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

app.controller("UserController",function ($scope, $http, $rootScope, $window){

  $scope.user = {};
    $scope.singinUser = function() {
        $http({
            method : 'POST',
            url : '/api/login',
            data : $scope.user
        })
        .then(function successCallback(data) {
          $rootScope.userObj=data.data;
          $(".message").addClass("active");
          $("#message_head").text("Welcome");
          $("#message_text").text("sing in was completed")
          $('[showform]').each(function(num,elem) {
            if(elem.getAttribute("showform") =="True"){
              elem.style="diplay:block"
            }
            else{
               elem.style="diplay:none"
            }
          });         
        },
        function errorCallback(data) {
          $(".message").addClass("active");
          $("#message_head").text("Sorry");
          $("#message_text").text(data.data.status || "Error")
          
        })
        

}
})
app.controller("RegistrCtrl",function ($scope, $http,$rootScope){
  $scope.newUser = {};
    $scope.singupUser = function() {
      console.log($scope.newUser)
        $http({
            method : 'POST',
            url : '/api/register',
            data : $scope.newUser
        })
        .then(function successCallback(data) {
          $rootScope.userObj=data.data;
          $(".message").addClass("active");
          $("#message_head").text("Welcome");
          $("#message_text").text("registration was completed")
          
        },
        function errorCallback(data) {
          $(".message").addClass("active");
          $("#message_head").text("Sorry");
          $("#message_text").text(data.data.status || "Something was wrong")
        })
}
})
app.controller("logOutUser",function ($scope,$window,$rootScope){
  $scope.logOut=function (){
    $rootScope.userObj= undefined
    $window.location="/logout"
     /*logout*/
  }
})

app.controller('LoginCtrl', ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){

  $scope.showLoginModal = false;
  $scope.toggleLoginModal = function(){
    $scope.showLoginModal = !$scope.showLoginModal;
  };

  $scope.showRegisterModal = false;
  $scope.toggleRegisterModal = function(){
    $scope.showRegisterModal = !$scope.showRegisterModal;
  };  

  $scope.logined = false;
  $rootScope.Logined = function(){
    return $scope.logined;
  };

  $rootScope.userObj = {};
  $rootScope.setUserObj = function(data){
    $rootScope.userObj = data;
  };

  $scope.newUser = {}

  $scope.registerError = "";
  $scope.loginError = "";
  $scope.setError = function(error){
    $scope.registerError = error;
  }
  $scope.setLoginError = function(error){
    $scope.loginError = error;
  }

  $scope.Register = function(){
    if($scope.newUser.password == $scope.newUser.pass_confirm){
      $http({
        method: 'POST',
        url: '/api/register',
        data: $scope.newUser
      }).then(function successCallback(responce){
        $scope.showRegisterModal = false;
        // $scope.logined = true;
        // $scope.setUserObj(responce.data);
        // add showing user data 
        console.log(responce.data);
        $scope.user.email = $scope.newUser.email;
        $scope.user.password = $scope.newUser.password;
        $scope.Login();
        $scope.newUser = {};
      },
        function errorCallback(data){
          $scope.wrongCredentials = true;
            $scope.setError(data.data['error'] || data.data['status'])
        });
    }else{
      $scope.setError("Passwords don't match!!!");      
    }
  };

  $scope.user = {};
  $scope.Login = function(){
    $http({
      method: 'POST',
      url: '/api/login',
      data: $scope.user
    }).then(function successCallback(responce){
      $scope.showLoginModal = false;
      $scope.logined = true;
      $scope.setUserObj(responce.data);
      $scope.user = {};
      // add showing user data 
    },
      function errorCallback(data){
          $scope.wrongLoginCredentials = true;
          $scope.setLoginError(data.data['error'] || data.data['status'])
      });
  };

  $scope.Logout = function(){
    $http({
      method: 'POST',
      url: '/api/logout',
      data: $scope.user
    }).then(function successCallback(responce){
      $scope.logined = false;
      $scope.setUserObj({});
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