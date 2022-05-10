function get_query(){
    let url = document.location.href;
    let qs = url.substring(url.indexOf('?') + 1).split('&');
    for(var i = 0, result = {}; i < qs.length; i++){
        qs[i] = qs[i].split('=');
        result[qs[i][0]] = decodeURIComponent(qs[i][1]);
    }
    return result;
}

function updateBox(){
    let result = get_query();

    let num = result['num'];
    let url = $('#url').val();
    let title = $('#title').val();
    let ctype = $('#ctype').val();
    let star = $('#star').val();
    let comment = $('#comment').val();
    /* NULL CHECK */
    if(comment == ''){
        alert("comment IS NULL");
        return;
    }
    if(star == '-- 선택하기 --'){
        alert("SELECT STAR");
        return;
    }

    $.ajax({
        type: 'PUT',
        url: '/culture',
        data: {num_give : num, url_give: url, star_give: star, comment_give: comment, title_give: title, ctype_give: ctype},
        success: function (response) {
            alert(response['msg'])
            opener.window.location.reload("/");
            window.close();
        }
    });
}

function closeBox(){
    close();
}
