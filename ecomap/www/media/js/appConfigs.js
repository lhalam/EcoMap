app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
  $routeProvider
   .when('/', {
    redirectTo: '/map'
  })
   .when('/map', {
    templateUrl: '/templates/map.html',
    controller: 'MapCtrl'
  })
  .when('/user_profile', {
    templateUrl: '/templates/userProfile.html',
    controller: 'UserProfileCtrl'
  });
  // .when('/login', {
  //   templateUrl: '/templates/login/html',
  //   controller: 'UserManagementCtrl'
  // });

  // $locationProvider.html5Mode({
  //   enabled: true,
  //   requireBase: false
  // });
}]);
