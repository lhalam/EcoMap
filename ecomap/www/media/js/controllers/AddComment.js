app.controller('AddComment', ['$scope', '$http', 'toaster', '$state',
  function($scope, $http, toaster, $state) {
    $scope.post_comment = function() {
      alert($scope.comment_text);
    }
  }
]);