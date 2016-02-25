app.filter('dictFilter', function (dict) {
  return function (item) {
    if (item in dict) {
    	return dict[item];
    }
  };
});

app.filter('answerFilter',function (answer) {
    return function(count){
        if (count <5){
            return count + ' ' + answer[count];
        }
        else if (count >= 5 && count <= 20){
            return count + ' ' + answer['other'];
        }
        else {
            count = String(count);
            last_num = count.substr(count.length - 1);
            return count + ' ' + (answer[last_num] || answer['other']);
        }
    };
});