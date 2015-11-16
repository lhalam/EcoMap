var app=angular.module('app',['ui.bootstrap', 'ngCookies', 'ngMessages', 'satellizer']);

app.config(function($authProvider) {

            // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/api/login';

            // Redirect to the auth state if any other states
            // are requested other than users
            // $urlRouterProvider.otherwise('/auth');

        });
// app.controller('LoginCtrl', ['$scope','$authProvider', function($scope, $authProvider){

    
// }])