app.config(['$stateProvider', '$urlRouterProvider', '$authProvider',
 function($stateProvider, $urlRouterProvider, $authProvider) {

  // var accessRestrictionHandler = function($q, $rootScope, $state, $cookies) {
  //           var deferred = $q.defer();

  //           asyncCheckForLogin(function(status) {
  //               if ($cookies.get('role') != 'admin') {
  //                   $state.go("error403");
  //               }
  //               else
  //                   deferred.resolve();
  //           }.bind(this));

  //           return deferred.promise;
  //       };

  $stateProvider
    .state('user_profile', {
      abtract: true,
      url: '/user_profile',
      templateUrl: '/templates/userProfile.html',
      controller: 'UserProfileCtrl'
    })
    .state('user_profile.info', {
      url: '/info',
      templateUrl: '/templates/profileUserInfo.html'
    })
    .state('user_profile.problems', {
      url: '/problems',
      templateUrl: '/templates/profileProblems.html'
    })
    .state('user_profile.comments', {
      url: '/comments',
      templateUrl: '/templates/profileComments.html'
    })
    .state('user_profile.faq', {
      url: '/faq',
      templateUrl: '/templates/profileFaqEdit.html'
    })
    .state('map', {
      url: '/map',
      templateUrl: '/templates/map.html',
      controller: 'MapCtrl'
    })
    .state("admin", {
      abtract: true,
      url:"/admin",
      templateUrl:"/templates/admin.html",
      controller: 'AdminCtrl'
    })
    .state("admin.resources", {
      url: "/resources",
      templateUrl: "/templates/resourcesAdmin.html",
      controller: 'ResourceCtrl'
    })
    .state("admin.permissions", {
      url: "/permissions",
      templateUrl: "/templates/permissionAdmin.html",
      controller: 'PermisionCtrl'
    })
    .state("admin.roles", {
      url: "/roles",
      templateUrl: "/templates/rolesAdmin.html",
      controller: 'RoleCtrl'
    })
    .state("admin.users", {
      url: "/users",
      templateUrl: "/templates/userAdmin.html",
      controller: 'UserCtrl'
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
    .state('error403', {
      url: '/error403',
      templateUrl: '/templates/403.html'
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
    //.state('addProblem', {
    //  url: '/addProblem',
    //  onEnter: ['$stateParams', '$state', '$uibModal', function($stateParams, $state, $uibModal) {
    //    $uibModal.open({
    //        templateUrl: '/templates/addProblem.html',
    //        controller: 'addProblemCtrl'
    //    }).result.finally(function() {
    //        $state.go('map');
    //    });
    //  }]
    //})
    .state('addProblem', {
      url: '/addProblem',
        templateUrl: '/templates/addProblem.html',
        controller: 'addProblemCtrl'
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
    });
    
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