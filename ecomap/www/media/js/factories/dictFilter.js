app.filter('dictFilter', function (dict) {
  return function (item) {
    if (item in dict) {
    	return dict[item];
    }
  };
});

app.filter('answerFilter',function (answer) {
    return function(count){
        var countAnswer;
        if (count < 5){
            countAnswer = count + ' ' + answer[count];
        }
        else if (count >= 5 && count <= 20){
            countAnswer = count + ' ' + answer['other'];
        }
        else {
            count = String(count);
            last_num = count.substr(count.length - 1);
            countAnswer = count + ' ' + (answer[last_num] || answer['other']);
        }
        return countAnswer;
    };
});