"use strict";


function All() {
    listing()
}

function theater() {
    getctype('theater')
}

function movies() {
    getctype('movies')
}

function consert() {
    getctype('consert')
}


function login() {
    let val = $('#loginBtn').text();
    if (val === '로그인') {
        window.location.href = '/login';
    }
    if (val === '로그아웃') {
        let cookies = $.cookie();
        for (var cookie in cookies) {
            $.removeCookie(cookie);
        }
        window.location.reload();
    }
}

function sign_up() {
    window.location.href = '/signup';

}

function checkStatus() {
    let status = $.cookie('mytoken');
    if (status) {
        $('#loginBtn').text('로그아웃');

        $('#signUpBtn').css('display', 'none');
    } else {
        $('#loginBtn').text('로그인');
    }
}

$(document).ready(function () {
    listing();
    checkStatus();
}, {once: true});

function getctype(str) {
    $('#card-box').empty()
    $.ajax({
        type: "GET",
        url: `/culture/ctype?str=${str}`,
        data: {},
        success: function (response) {
            let rows = response['posting']
            console.log(rows)
            for (let i = 0; i < rows.length; i++) {
                let num = rows[i]['num'];
                let title = rows[i]['title']
                let url = rows[i]['url']
                let star = rows[i]['star']
                let comment = rows[i]['comment']


                let star_image = '⭐'.repeat(star)


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


function open_box() {
     if ($.cookie('mytoken')) {
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

    } else {
        alert('로그인해주세요')
        return;
    }

    $('#post-box').show()


}

function close_box() {
    $('#post-box').hide()
}

function deleat() {
    $('')
}


function listing() {
    $.ajax({
        type: 'GET',
        url: '/culture',
        data: {},
        success: function (response) {
            $('#card-box').empty();
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

// function open_box() {
//     $('#post-box').show()
// }
//
// function close_box() {
//     $('#post-box').hide()
// }

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

