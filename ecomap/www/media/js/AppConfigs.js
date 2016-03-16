app.config(['$stateProvider', '$urlRouterProvider', '$authProvider',
 function($stateProvider, $urlRouterProvider, $authProvider ) {
  $stateProvider
  .state('error404', {
    url: '/error404',
    templateUrl: '/templates/404.html'
  })
  .state('error403', {
    url: '/error403',
    templateUrl: '/templates/403.html'
  })
  .state('user_profile', {
    abtract: true,
    url: '/user_profile',
    templateUrl: '/templates/userProfile.html',
    controller: 'UserProfileCtrl',
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'authenticated', state: 'error403'});
      }
    }
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
  .state('user_profile.subscriptions', {
    url: '/subscriptions',
    templateUrl: '/templates/profileSubscriptions.html'
  })
  .state('user_profile.faq', {
    url: '/faq',
    templateUrl: '/templates/profileFaqEdit.html',
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'admin', state: 'error403'});
      }
    }
  })
  .state('map', {
    url: '/map',
    templateUrl: '/templates/map.html',
    controller: 'MapCtrl'
  })
  .state('admin', {
    abtract: true,
    url: '/admin',
    templateUrl: '/templates/admin.html',
    controller: 'AdminCtrl',
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'admin', state: 'error403'});
      }
    }
  })
  .state('admin.resources', {
    url: '/resources',
    templateUrl: '/templates/resourcesAdmin.html',
    controller: 'ResourceCtrl'
  })
  .state('admin.permissions', {
    url: '/permissions',
    templateUrl: '/templates/permissionAdmin.html',
    controller: 'PermisionCtrl'
  })
  .state('admin.roles', {
    url: '/roles',
    templateUrl: '/templates/rolesAdmin.html',
    controller: 'RoleCtrl'
  })
  .state('admin.users', {
    url: '/users',
    templateUrl: '/templates/userAdmin.html',
    controller: 'UserCtrl'
  })
  .state('admin.problems', {
    url: '/problems',
    templateUrl: '/templates/problemsAdmin.html',
    controller: 'ProblemCtrl'
  })
  .state('admin.tempdata', {
    url: '/tempdata',
    templateUrl: '/templates/tempdataAdmin.html',
    controller: 'TempDataCtrl'
  })
  .state('faq', {
    url: '/faq/:faqAlias',
    templateUrl: '/templates/detailedFaq.html',
    controller: 'DetailedFaqCtrl'
  })
  .state('addFaq', {
    url: '/addFaq',
    templateUrl: '/templates/addFaq.html',
    controller: 'AddFaqCtrl',
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'admin', state: 'error403'});
      }
    }
  })
  .state('editProblem', {
    url: '/editProblem/:id',
    templateUrl: '/templates/editProblem.html',
    controller: 'EditProblemCtrl'
  })
  .state('editFaq', {
    url: '/editFaq/:alias',
    templateUrl: '/templates/editFaq.html',
    controller: 'EditFaqCtrl',
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'admin', state: 'error403'});
      }
    }
  })
  .state('statistic', {
    url: '/statistic',
    templateUrl: '/templates/statistic.html'
  })
  .state('addProblem', {
    url: '/addProblem',
    views:{
      'sidebar': {
        'templateUrl': '/templates/addProblem.html',
        'controller': 'AddProblemCtrl'
      },
      '': {
        'templateUrl': '/templates/map.html',
        'controller': 'MapCtrl'
      }
    },
    resolve: {
      admin: function(grant) {
        return grant.only({test: 'authenticated', state: 'error403'});
      }
    }
  })
  .state('detailedProblem', {
    url: '/detailedProblem/:id',
    views: {
      'sidebar': {
        'templateUrl': '/templates/detailedProblem.html',
        'controller': 'DetailedProblemCtrl'
      },
      '': {
        'templateUrl': '/templates/map.html',
        'controller': 'MapCtrl'
      }
    }
    })
    .state('login', {
      url: '/login',
      templateUrl: '/templates/login.html',
      controller: 'LoginCtrl'
    })
    .state('restore_email', {
      url: '/restore_email',
      templateUrl: '/templates/password_restoring_email.html',
      controller: 'RestorePasswordCtrl'
    })
    .state('restore_pass', {
      url: '/restore_password/:hash_sum',
      templateUrl: '/templates/password_restoring_pass.html',
      controller: 'RestorePasswordCtrl'
    })
    .state('registerAdmin', {
      url: '/addUserByAdmin',
      templateUrl: '/templates/RegisterUserByAdmin.html',
      controller: 'AddUserByAdmin'
    })
    .state('userDeleteConfirmation', {
      url: '/userConfirm?hash_sum',
      controller: 'userDeleteConfirmation'
    })
    .state('register', {
      url: '/register',
      templateUrl: '/templates/register.html',
      controller: 'RegisterCtrl'
    });

    $urlRouterProvider.otherwise('map');
    $authProvider.loginUrl = '/api/login';
    $authProvider.signupUrl = '/api/register';
    $authProvider.facebook({
      clientId: '1000437473361749',
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
