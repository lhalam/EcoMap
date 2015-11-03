var myApp = angular.module('myApp', ['ngRoute']);

myApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      access: {restricted: true}
    })
    .when('/login', {
      controller: 'loginController',
      access: {restricted: false}
    })
    .when('/logout', {
      controller: 'logoutController',
      access: {restricted: true}
    })
    .when('/register', {
      controller: 'registerController',
      access: {restricted: false}
    })

    .otherwise({redirectTo: '/'});
});

myApp.run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    if (next.access.restricted && AuthService.isLoggedIn() === false) {
      $location.path('/login');
      $route.reload();
    }
  });
});

var app = angular.module("app", []);

app.controller("MyCtrl",function MyCtrl($scope,$http,$location,$window){
	$scope.name="Vlad"
	$scope.show=function (){
		console.log("show")
	}

})