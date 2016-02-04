 app.directive('availableEmail', function($http) {
   var toId;
   return {
     restrict: 'A',
     require: 'ngModel',
     link: function(scope, elem, attr, ctrl) {
       scope.$watch(attr.ngModel, function(value) {
         if (toId) clearTimeout(toId);
         toId = setTimeout(function() {
           if(scope.newUser.email) {
             $http({
               url: '/api/email_exist',
               method: 'POST',
               data: scope.newUser
             })
             .then(function successCallback(responce) {
               ctrl.$setValidity('availableEmail', !responce.data['isValid']);
             },
             function errorCallback(responce) {});
           }
         }, 200);
       })
     }
   }
 });

app.directive('compareTo', function() {
    return {
        require: 'ngModel',
        scope: {
            otherModelValue: '=compareTo'
        },
        link: function(scope, element, attributes, ngModel) {
            ngModel.$validators.compareTo = function(modelValue) {
                return modelValue == scope.otherModelValue;
            };
            scope.$watch('otherModelValue', function() {
                ngModel.$validate();
            });
        }    
      }
});
