app.run(['grant', '$auth', '$cookies', '$log',
  function(grant, $auth, $cookies, $log) {
    grant.addTest('admin', function() {
      var result = null;
      if ($auth.isAuthenticated() && $cookies.get('role') == 'admin') {
        result = true;
      }
      return result;
    });

    grant.addTest('authenticated', function(){
      var result = null;
      if($auth.isAuthenticated()){
        result = true;
      }
      return result;
    });
  }
]);