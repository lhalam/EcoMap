app.factory('msgError', function(toaster) {
  return msgError = {
    'alreadyExist': 'Дане ім’я вже зарезервоване.',
    'alreadyBinded': 'Так як дані вже прив’язані.',
    'incorectData': 'Так як дані невірні.',
    'incorrectPhoto': ' Неправильний формат фото.',
    'incorrectSize': ' Розмір файлу не повинен перевищувати 200 кілобайт.',
    'couldntDelete': ' Файл не видалено.'
  }
})
