app.config(['$stateProvider', '$urlRouterProvider', '$authProvider', function($stateProvider, $urlRouterProvider, $authProvider) {

  $stateProvider
    .state('user_profile', {
      url: '/user_profile',
      templateUrl: '/templates/userProfile.html',
      controller: 'UserProfileCtrl'
    })
    .state('map', {
      url: '/map',
      templateUrl: '/templates/map.html',
      controller: 'MapCtrl'
    })
    .state('admin', {
      url: '/admin',
      templateUrl: '/templates/admin.html',
      controller: 'AdminCtrl'
    })
    .state('faq', {
      url: '/faq/:faqAlias',
      templateUrl: '/templates/detailedFaq.html',
      controller: 'DetailedFaqCtrl'
    })
    .state('addFaq', {
      url: '/addFaq',
      templateUrl: '/templates/addFaq.html',
      controller: 'AddFaqCtrl'
    })
    .state('editFaq', {
      url: '/editFaq/:alias',
      templateUrl: '/templates/editFaq.html',
      controller: 'EditFaqCtrl'
    })
    .state('error404', {
      url: '/error404',
      templateUrl: '/templates/404.html'
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
    }
    )
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
    .state('admin_resource',{
      url:"/admin/resource"
    })
    ;
    
    $urlRouterProvider.otherwise('/map');
    $authProvider.loginUrl = '/api/login';
    $authProvider.signupUrl = '/api/register';
    $authProvider.facebook({
      clientId: '1525737571082521',
      url: '/api/authorize/facebook',
      name: 'facebook',
      authorizationEndpoint: 'https://www.facebook.com/v2.5/dialog/oauth',
      redirectUri: window.location.origin + '/',
      requiredUrlParams: ['display', 'scope'],
      scope: ['email'],
      scopeDelimiter: ',',
      display: 'popup',
      type: '2.0',
      popupOptions: { width: 580, height: 400 }
    });  

}]);
