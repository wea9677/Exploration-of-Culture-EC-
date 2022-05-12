import certifi
import jwt
import requests
from pymongo import MongoClient

import datetime
import hashlib
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, url_for, redirect


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

ca = certifi.where()

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb+srv://wea9677:tmxkdlfl@cluster0.xmzro.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.dbsparta


# ----- main -----
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

# -----login, register-----
@app.route('/login')
def login():
    msg = request.args.get("msg")

    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(token)

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)

    return jsonify({'result': 'success'})



@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})



@app.route('/culture/update')
def update():
    num = request.args.get('num')
    return render_template('update.html', num=num)


@app.route('/culture', methods=['POST'])
def web_culture_post():
    id_receive = request.form['id_give']
    url_recevie = request.form['url_give']
    title_recevie = request.form['title_give']
    star_recevie = request.form['star_give']
    comment_recevie = request.form['comment_give']

    ctype_recevie = request.form['ctype_give']

    culture_list = list(db.culture.find({}, {'_id': False}))
    if len(culture_list) == 0:
        count = len(culture_list) + 1
    else:
        count = culture_list[len(culture_list) - 1]['num'] + 1
    doc = {
        'user':id_receive,
        'num': count,
        'title': title_recevie,
        'url': url_recevie,
        'star': star_recevie,
        'comment': comment_recevie,
        'ctype': ctype_recevie
    }

    db.culture.insert_one(doc)
    doc = {
        'num': count,
        'like': 0
    }
    db.cultureLike.insert_one(doc)
    return jsonify({'msg': '기록 완료!'})


@app.route('/culture', methods=['GET'])
def web_culture_get():
    post_list = list(db.culture.find({}, {'_id': False}))

    return jsonify({'posting': post_list})


@app.route('/culture/ctype', methods=['GET'])
def web_culture_gettype():
    ctype = request.args.get('str')
    post_list = list(db.culture.find({'ctype': ctype}, {'_id': False}))

    return jsonify({'posting': post_list})


@app.route("/culture", methods=["PUT"])
def movie_update():
    num_receive = request.form['num_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    title_receive = request.form['title_give']
    ctype_receive = request.form['ctype_give']

    if url_receive is None:
        db.culture.update_one({'num': int(num_receive)},
                              {'$set': {'star': star_receive, 'comment': comment_receive, 'title': title_receive,
                                        'ctype': ctype_receive}});
    else:
        db.culture.update_one({'num': int(num_receive)},
                              {'$set': {'url': url_receive, 'star': star_receive, 'comment': comment_receive,
                                        'title': title_receive, 'ctype': ctype_receive}});

    return jsonify({'msg': '수정 완료!'});


@app.route("/culture", methods=["DELETE"])
def movie_delete():
    num_receive = request.form['num_give']
    db.culture.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'});

@app.route('/culture/like', methods=["POST"])
def card_like():
    num_receive = request.form['num_give']
    action_receive = request.form['action_give']

    card = db.cultureLike.find_one({'num':int(num_receive)}, {'_id':False})
    like = card['like']

    if action_receive == 'like':
        like += 1
        db.cultureLike.update_one({'num':int(num_receive)}, {'$set': {'like': int(like)}})
        return jsonify({'result': 'success'})
    else:
        if like != 0:
            like -= 1
            db.cultureLike.update_one({'num': int(num_receive)}, {'$set': {'like': int(like)}})
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'success'})

@app.route('/culture/like', methods=['GET'])
def card_getLike():
    num_receive = request.args.get('num_give')
    if num_receive != 'undefined' :
        card = db.cultureLike.find_one({'num': int(num_receive)}, {'_id':False})
        print(card)
        return jsonify({'like': card['like']})
    else:
        return jsonify()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
