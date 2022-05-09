from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://wea9677:tmxkdlfl@cluster0.xmzro.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')


@app.route('/ec', methods=['POST'])
def web_ec_post():
   url_recevie = request.form['url_give']
   title_recevie = request.form['title_give']
   star_recevie = request.form['star_give']
   comment_recevie = request.form['comment_give']

   # 1. 다 가져와서 데이터를 저장해놓고 사용하는 방법
   # 2. 그때그때 db.select();

   doc = {
      'url': url_recevie,
      'sort': 'movie',
      'title': title_recevie,
      'star': star_recevie,
      'comment': comment_recevie
   }

   db.cultures.insert_one(doc)
   return jsonify({'msg' : '기록 완료!'})

@app.route('/ec', methods=['GET'])
def web_ec_get():
   post_list = list(db.movies.find({}, {'_id': False}))

   return jsonify({'posting': post_list})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
