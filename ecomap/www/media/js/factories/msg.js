app.factory('msg', function(toaster) {
  return msg = {
    editSuccess: function(msg) {
      toaster.pop('success', 'Редагування', 'Редагування ' + msg + ' здійснено успішно!');
    },
    deleteSuccess: function(msg) {
      toaster.pop('success', 'Видалення', 'Видалення ' + msg + ' здійснено успішно!');
    },
    createSuccess: function(msg) {
      toaster.pop('success', 'Додавання', 'Додавання ' + msg + ' здійснено успішно!');
    },
    editError: function(msg, type) {
      toaster.pop('error', 'Редагування', 'При редагуванні ' + msg + ' виникла помилка!' + type);
    },
    deleteError: function(msg, type) {
      toaster.pop('error', 'Видалення', 'При видаленні ' + msg + ' виникла помилка!' + type);
    },
    createError: function(msg, type) {
      toaster.pop('error', 'Додавання', 'При додаванні ' + msg + ' виникла помилка!' + type);
    },
  };
});
