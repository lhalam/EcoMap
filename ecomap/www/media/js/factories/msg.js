app.factory('msg', function (toaster) {
    return msg = {
        editSuccess: function(msg){
            toaster.pop('success', 'Редагування', 'Редагування ' + msg + ' здійснено успішно!');
        },
        deleteSuccess: function(msg){
            toaster.pop('success', 'Видалення', 'Видалення ' + msg + ' здійснено успішно!');
        },
        createSuccess: function(msg){
            toaster.pop('success', 'Додавання', 'Додавання ' + msg + ' здійснено успішно!');
        },
        editError: function(msg){
            toaster.pop('error', 'Редагування', 'При редагуванні ' + msg + ' виникла помилка!');
        },
        deleteError: function(msg){
            toaster.pop('error', 'Видалення', 'При видаленні ' + msg + ' виникла помилка!');
        },
        createError: function(msg){
            toaster.pop('error', 'Додавання', 'При додаванні ' + msg + ' виникла помилка!');
        },
    };
    });