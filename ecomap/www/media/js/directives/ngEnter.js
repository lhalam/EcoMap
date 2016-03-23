app.directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                    if (!event.shiftKey) {
                        scope.$apply(function(){
                            scope.$eval(attrs.ngEnter, {'event': event});
                        });
                        event.preventDefault();
                    }
                }
            });
        };
    });

app.directive('ngEsc', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress keyup", function (event) {
            if(event.which === 27) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEsc);
                });
                event.preventDefault();
            }
        });
    };
});

app.directive('ngContent', [
    function() {
      return {
        link: function($scope, $el, $attrs) {
                $scope.$watch($attrs.ngContent, function(value) {
                  $el.attr('content', value);
                });
              }
      };
    }
  ])
;
