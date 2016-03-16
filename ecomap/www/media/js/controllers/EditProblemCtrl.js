app.controller('EditProblemCtrl', ['$scope', '$stateParams', '$http', 'toaster', '$state',  '$cookies',
  function($scope, $stateParams, $http, toaster, $state, $cookies) {
    $scope.severities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];    
/*   if ($cookies.get('role')=='user') {
      $scope.hideSeverityForUser = false;
    }  else  $scope.hideSeverityForUser = true;*/
    $scope.hideSeverityForUser = $cookies.get('role')=='user' ? false : true;
    $scope.statuses = ['Не вирішено', 'Вирішено'];
    $scope.page = {};
    $scope.editPage = function(page) {
      $http({
        method: 'PUT',
        url: '/api/editResource/' + page.id,
        data: page
      }).then(function successCallback(response) {
        toaster.pop('success', 'Проблему відредаговано', 'Проблему відредаговано успішно!');
        $state.go('user_profile.faq');
      }, function errorCallback() {
        toaster.pop('error', 'Помилка', 'Проблему не вдалось відредагувати через помилку!');
      });
    };


/*    $scope.loadPage = function(alias) {
      $http({
        method: 'GET',
        url: '/api/resources/' + alias
      }).then(function successCallback(response) {
        $scope.page.title = response.data[0].title;
        $scope.page.alias = response.data[0].alias;
        $scope.page.description = response.data[0].description;
        $scope.page.content = response.data[0].content;
        $scope.page.meta_keywords = response.data[0].meta_keywords;
        $scope.page.meta_description = response.data[0].meta_description;
        $scope.page.is_enabled = response.data[0].is_enabled;
        $scope.page.id = response.data[0].id;
      }, function errorCallback() {})
    };
    $scope.loadPage($stateParams.alias);*/
  }
]);
