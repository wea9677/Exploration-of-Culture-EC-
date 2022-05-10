from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://wea9677:tmxkdlfl@cluster0.xmzro.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)

db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


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

    # if ctype == 'all':
    #    post_list = list(db.culture.find({}, {'_id': False}))
    # else:
    #    post_list = list(db.culture.find({}, {'_id': False, 'ctype': ctype}))

    return jsonify({'posting': post_list})

@app.route("/culture", methods=["PUT"])
def movie_update():
    num_receive = request.form['num_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    if url_receive is None :
        db.culture.update_one({'num': int(num_receive)},
                             {'$set': {'star': star_receive, 'comment': comment_receive}});
    else:
        db.culture.update_one({'num': int(num_receive)},
                             {'$set': {'url': url_receive, 'star': star_receive, 'comment': comment_receive}});

    return jsonify({'msg': '수정 완료!'});

@app.route("/culture", methods=["DELETE"])
def movie_delete():
    num_receive = request.form['num_give']
    db.culture.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'});


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
