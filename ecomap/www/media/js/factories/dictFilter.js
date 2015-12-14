app.filter('dictFilter', function (dict) {
  return function (item) {
    if(item in dict){
    	return dict[item]
    }
  };
});