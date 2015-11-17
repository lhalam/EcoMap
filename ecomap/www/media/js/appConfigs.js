app.config(['$stateProvider', '$urlRouterProvider', '$authProvider', function($stateProvider, $urlRouterProvider, $authProvider) {

  $urlRouterProvider.otherwise('/map');

  $stateProvider
    .state('map', {
      url: '/map',
      templateUrl: '/templates/map.html',
      controller: 'MapCtrl'
    })
    .state('user_profile', {
      url: '/user_profile',
      templateUrl: '/templates/userProfile.html',
      controller: 'UserProfileCtrl'
    })
    .state('admin', {
      url: '/admin',
      templateUrl: '/templates/admin.html',
      controller: 'AdminCtrl'
    })
    .state('login', {
      url: '/login',
      onEnter: ['$stateParams', '$state', '$uibModal', function($stateParams, $state, $uibModal) {
        $uibModal.open({
            templateUrl: '/templates/login.html',
            controller: 'LoginCtrl',
        }).result.finally(function() {
            $state.go('map');
        });
    }]
    })
    .state('register', {
      url: '/register',
      onEnter: ['$stateParams', '$state', '$uibModal', function($stateParams, $state, $uibModal) {
        $uibModal.open({
            templateUrl: '/templates/register.html',
            controller: 'RegisterCtrl',
        }).result.finally(function() {
            $state.go('map');
        });
    }]
    })
    
    $authProvider.loginUrl = '/api/login';
    $authProvider.signupUrl = '/api/register';    

}]);
