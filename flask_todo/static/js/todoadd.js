//フォームのsubmitを拾う
$('#ajax-add').on('click', function(event){
    //通常のアクションをキャンセルする
    event.preventDefault();

    // 未入力は無視
    if($('#input-data').val() === ''){
        console.log("skip!");
        return false;
    }

    $form = $(this).parents('form:first');
    var addData = $form.serialize(); //add={入力内容}

    $.ajax({
        url: '/post',
        type: 'POST',
        data: addData
    })
    .then(
        // 1つめは通信成功時のコールバック
        function (data) {
            console.log("success!");
            $('#input-data').val('');
            var word = JSON.parse(data);
            word = word["word"];
            var addHtml = '<p><label><input type="checkbox" name="delwords" value="'+word+'">'+word+'</label></p>';
            $('#todolist').append(addHtml);
        },
        // 2つめは通信失敗時のコールバック
        function () {
            console.log("fail!");
            alert("通信エラー");
        }
    );

});
