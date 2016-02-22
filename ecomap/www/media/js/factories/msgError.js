app.factory('msgError', function(toaster) {
  return msgError = {
    'alreadyExist': 'Дане ім’я вже зарезервоване.',
    'alreadyBinded': 'Так як дані вже прив’язані.',
    'incorectData': 'Так як дані невірні.',
    'wrongData': 'Файл вже існує або не вірний формат файлу.'
  }
})
