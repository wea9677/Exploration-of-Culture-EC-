"use strict";


function listing() {
    $.ajax({
        type: 'GET',
        url: '/culture',
        data: {},
        success: function (response) {
            $('#cards-box').empty();
            let rows = response['posting']
            console.log(rows);
            for (let i = 0; i < rows.length; i++) {
                let num = rows[i]['num'];
                let title = rows[i]['title']
                let url = rows[i]['url']
                let star = rows[i]['star']
                let comment = rows[i]['comment']

                let star_image = '⭐'.repeat(star);

                let temp_html = `<div class="col card-box">
                                 <div class="card h-100">
                                     <img src="${url}" class="card-img-top">
                                     <div class="card-body">
                                         <h5 class="card-title">${title}</h5>
                                         <p>${star_image}</p>
                                         <p class="mycomment">${comment}</p>
                                     </div>
                                 </div>
                                 <div class="option">
                                     <a href="#" onclick="updateCard(${num});"><span class="las la-edit"></span></a>
                                     <a href="#" onclick="dropList(${num});"><span class="las la-trash"></span></a>
                                 </div>
                            </div>`;

                $('#card-box').append(temp_html);
            }
        }
    })
}

function posting() {
    let url = $('#url').val()
    let title = $('#title').val()
    let star = $('#star').val()
    let comment = $('#comment').val()
    let ctype = $('#ctype').val()

    /* NULL CHECK */
    if (url == '') {
        alert("URL IS NULL");
        return;
    }
    if (comment == '') {
        alert("comment IS NULL");
        return;
    }
    if (star == '-- 선택하기 --') {
        alert("SELECT STAR");
        return;
    }

    $.ajax({
        type: 'POST',
        url: '/culture',
        data: {url_give: url, title_give: title, star_give: star, comment_give: comment, ctype_give: ctype},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function open_box() {
    $('#post-box').show()
}

function close_box() {
    $('#post-box').hide()
}

function dropList(n) {
    $.ajax({
        type: 'DELETE',
        url: `/culture`,
        data: {num_give: n},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });
}

function updateCard(n) {
    window.open(`http://localhost:5000/culture/update?num=${n}`, 'new', 'scrollbars=yes,resizable=no width=640 height=560, left=0,top=0\');return false')
}

