app.factory('dict', function(toaster) {
  return {
  	'GET': 'Отримати',
  	'PUT': 'Змінити',
  	'POST': 'Надіслати',
  	'DELETE': 'Видалити',
  	'Any': 'Всі',
  	'Own': 'Свої',
  	'None': 'Жодні',
  };
});

app.factory('answer', function(toaster){
    return {   
        '1' : 'відповідь',
        '2' : 'відповіді',
        '3' : 'відповіді',
        '4' : 'відповіді',
        'other' : 'відповідей',
    };
});