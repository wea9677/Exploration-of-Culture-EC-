from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import jwt
import datetime
import hashlib
from datetime import datetime, timedelta
import certifi

ca = certifi.where()

SECRET_KEY = 'SPARTA'
client = MongoClient('mongodb+srv://wea9677:tmxkdlfl@cluster0.xmzro.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)

db = client.dbsparta



#-----login, register-----

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
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)





#-------main-------

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    return render_template('index.html')

@app.route('/culture/update')
def update():
   num = request.args.get('num')
   return render_template('update.html', num=num)

@app.route('/culture', methods=['POST'])
def web_culture_post():
    url_recevie = request.form['url_give']
    title_recevie = request.form['title_give']
    star_recevie = request.form['star_give']
    comment_recevie = request.form['comment_give']

    ctype_recevie = request.form['ctype_give']
    print(ctype_recevie)

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url_recevie, headers=headers)
    #
    # soup = BeautifulSoup(data.text, 'html.parser')
    #
    # og_image = soup.select_one('meta[property="og:image"]')
    #
    # url_recevie = og_image['content']
    # 1. 다 가져와서 데이터를 저장해놓고 사용하는 방법
    # 2. 그때그때 db.select();

    culture_list = list(db.culture.find({}, {'_id': False}))
    if len(culture_list) == 0:
        count = len(culture_list) + 1
    else:
        count = culture_list[len(culture_list) - 1]['num'] + 1
    doc = {
        'num': count,
        'title': title_recevie,
        'url': url_recevie,
        'star': star_recevie,
        'comment': comment_recevie,
        'ctype': ctype_recevie
    }

    db.culture.insert_one(doc)
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

    if url_receive is None :
        db.culture.update_one({'num': int(num_receive)},
                             {'$set': {'star': star_receive, 'comment': comment_receive, 'title':title_receive, 'ctype':ctype_receive}});
    else:
        db.culture.update_one({'num': int(num_receive)},
                             {'$set': {'url': url_receive, 'star': star_receive, 'comment': comment_receive, 'title':title_receive, 'ctype':ctype_receive}});

    return jsonify({'msg': '수정 완료!'});

@app.route("/culture", methods=["DELETE"])
def movie_delete():
    num_receive = request.form['num_give']
    db.culture.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'});


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)