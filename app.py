from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.6yhxk.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')


@app.route('/culture', methods=['POST'])
def web_ec_post():
   url_recevie = request.form['url_give']
   title_recevie = request.form['title_give']
   star_recevie = request.form['star_give']
   comment_recevie = request.form['comment_give']

   ctype_recevie = request.form['ctype_give']
   print(ctype_recevie)

   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_recevie, headers=headers)

   soup = BeautifulSoup(data.text, 'html.parser')

   og_image = soup.select_one('meta[property="og:image"]')

   url_recevie = og_image['content']

   # 1. 다 가져와서 데이터를 저장해놓고 사용하는 방법
   # 2. 그때그때 db.select();

   doc = {
      'url': url_recevie,
      'title': title_recevie,
      'star': star_recevie,
      'comment': comment_recevie,
      'ctype': ctype_recevie
   }

   db.movies.insert_one(doc)
   return jsonify({'msg' : '기록 완료!'})

@app.route('/culture', methods=['GET'])
def web_culture_get():

   post_list = list(db.movies.find({}, {'_id': False}))

   return jsonify({'posting': post_list})

@app.route('/culture/type', methods=['GET'])
def web_culture_gettype():



   ctype = request.args.get('str')
   post_list = list(db.culture.find({'ctype': ctype}, {'_id': False}))

   # if ctype == 'all':
   #    post_list = list(db.culture.find({}, {'_id': False}))
   # else:
   #    post_list = list(db.culture.find({}, {'_id': False, 'ctype': ctype}))

   return jsonify({'posting': post_list})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)