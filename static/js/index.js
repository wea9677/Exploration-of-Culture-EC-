"use strict";

/* get Token Data */
/* parseJwt($.cookie('mytoken')) 으로 사용하면 아이디 값이 전달된다. */
const parseJwt = (token) => {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

function All() {
    $('#top').css({'background-image': 'linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://post-phinf.pstatic.net/MjAyMTA1MjRfMTQ5/MDAxNjIxODM5NjMxODM4.x9oS0lZ2R2-uhe-FrdC7BjvGj2bYXcflkCwdxTv7ahgg.ryZCrIOTJaWEMYhegrYuHlXcVJdZaKb2Dtv_FbNi9Tkg.JPEG/%EA%B3%B5%EA%B0%90-%EC%A0%95%EC%B1%85%EC%A3%BC%EA%B0%84%EC%A7%80%EA%B3%B5%EA%B0%90-%EC%9D%B4%EB%82%A0%EC%B9%98-%EC%9D%B4%EB%82%A0%EC%B9%98%EB%B0%B4%EB%93%9C-%EB%B2%94%EB%82%B4%EB%A0%A4%EC%98%A8%EB%8B%A4-%ED%95%9C%EA%B5%AD%EA%B4%80%EA%B4%91%EA%B3%B5.jpg?type=w1200")'});
    $('#top').css({'background-size': 'cover'});
    $('#top').css({'background-position': 'center'});
    $('#top').css({'background-color': 'black'});

    listing()
}

function theater() {
    $('#top').css({'background-image': 'linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://assets.teenvogue.com/photos/5d34abc9d4f0850008e33d4f/16:9/w_2560%2Cc_limit/GettyImages-584925310.jpg")'});
    $('#top').css({'background-size': 'auto'});
    $('#top').css({'background-position': 'center 20%'});
    $('#top').css({'background-color': 'black'});

    getctype('theater')
}

function movies() {
    $('#top').css({'background-image': 'linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://image.ytn.co.kr/general/jpg/2022/0429/202204291112443922_t.jpg")'});
    $('#top').css({'background-size': 'cover'});
    $('#top').css({'background-position': 'center'});
    $('#top').css({'background-color': 'black'});

    getctype('movies')
}

function consert() {
    $('#top').css({'background-image': 'linear-gradient(0deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://i.pinimg.com/originals/e4/df/1a/e4df1a2dc175d8966557969d02d1c278.jpg")'});
    $('#top').css({'background-size': 'auto'});
    $('#top').css({'background-position': 'center 20%'});
    $('#top').css({'background-color': 'black'});
    $('#top').css({'background-repeat': 'no-repeat'});

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
    window.location.href = '/login?msg=signUp';
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
                let user = rows[i]['user'];
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
                                     <footer style="text-align: right">
                                        <div style="margin-right: 10px;">by <span style="font-weight: bold;">${user}</span>님</div>
                                     </footer>
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

function listing() {
    $.ajax({
        type: 'GET',
        url: '/culture',
        data: {},
        success: function (response) {
            $('#card-box').empty();
            let rows = response['posting']
            let num;
            console.log(rows);
            for (let i = 0; i < rows.length; i++) {
                let user = rows[i]['user'];
                num = rows[i]['num'];
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
                                     <div class="like-icon">
                                        <i id='likeBtn-${num}' style="display: none" class="like fa fa-heart" aria-hidden="true" onclick="javascript:like(${num}, 'dislike');"></i>
                                        <i id='dislikeBtn-${num}'  class="dislike fa fa-heart-o" aria-hidden="true" onclick="javascript:like(${num} , 'like');"></i>                                         
                                        <p id="getLike-${num}">0</p>
                                    </div>
                                     <footer style="text-align: right">
                                        <div style="margin-right: 10px;">by <span id="user" style="font-weight: bold;">${user}</span>님</div>
                                     </footer>
                                 </div>
                                 <div class="option">
                                     <a href="#" onclick="updateCard(${num});"><span class="las la-edit"></span></a>
                                     <a href="#" onclick="dropList(${num});"><span class="las la-trash"></span></a>
                                 </div>
                            </div>`;

                $('#card-box').append(temp_html);
                getlike(num);
            }

        }
    })
}

function posting() {
    let token = $.cookie('mytoken');
    let id = parseJwt(token).id;
    let url = $('#url').val()
    let title = $('#title').val()
    let star = $('#star').val()
    let comment = $('#comment').val()
    let ctype = $('#ctype').val()


    $.ajax({
        type: 'POST',
        url: '/culture',
        data: {id_give:id, url_give: url, title_give: title, star_give: star, comment_give: comment, ctype_give: ctype},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
        }
    });

}

function dropList(n) {
    let token = $.cookie('mytoken');
    let id = parseJwt(token).id;
    let acc = $('#user').text();
    if(id !== acc){
        alert('접근할 수 없습니다.')
        return;
    }
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
    let token = $.cookie('mytoken');
    let id = parseJwt(token).id;
    let acc = $('#user').text();

    if(id === acc)
        window.open(`http://localhost:5000/culture/update?num=${n}`, 'new', 'scrollbars=yes,resizable=no width=640 height=560, left=0,top=0\');return false')
    else{
        alert('접근할 수 없습니다.')
        return;
    }
}

function like(n, status){
    if(status == 'like'){
        $(`#likeBtn-${n}`).css('display', 'block');
        $(`#dislikeBtn-${n}`).css('display', 'none');
    }else{
        $(`#likeBtn-${n}`).css('display', 'none')
        $(`#dislikeBtn-${n}`).css('display', 'block');
    }
    $.ajax({
        type: 'POST',
        url: '/culture/like',
        data: {num_give: n, action_give:status},
        success: function (response) {
            if(response['result'] =='success'){
                getlike(n);
            }
        }
    });
}

function getlike(n){
    $.ajax({
        type: 'GET',
        url: `/culture/like?num_give=${n}`,
        data: {},
        success: function (response) {
            let num = parseInt(response['like']);
            $(`#getLike-${n}`).text(num);
        }
    });
}