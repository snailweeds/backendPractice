from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/review', methods=['POST']) # 리뷰 저장
def write_review():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/review', methods=['GET']) # 리뷰 보여주기
def read_reviews():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)