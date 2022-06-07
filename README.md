# serverPractice

Flask 프레임워크: 서버를 구동시켜주는 편한 코드 모음, 서버를 구동하려면 필요한 복잡한 일들을 쉽게 가져다 쓸 수 O
통상적으로 flask 서버를 돌리는 파일은 app.py라고 이름 짓기!

from flask import Flask --> 남들도 볼 수 있는 서버
app = Flask(__name__)

@app.route('/')  --> 서버 주소 뒤에 붙이는 것
def home():
   return 'This is Home!'  --> 출력되는 것 

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True) --> localhost:5000을 입력하면 'This is Home!' 출력됨
  
종료: 터미널 창을 클릭하시고, ctrl + c(ctrl + F2) 을 누르기

기본폴더구조(항상 이렇게 세팅) : 프로젝트 폴더 안에, (new>directory)
 ㄴstatic 폴더 (이미지, css파일을 넣어둡니다)
 ㄴtemplates 폴더 (html파일을 넣어둡니다)
 ㄴapp.py 파일
 
 import render_template
 return render_template('index.html')
 주의사항
 html파일 명 index.html로 통일
 
 * GET: 통상적으로! 데이터 조회(Read)를 요청할 때 예) 영화 목록 조회
       →  데이터 전달 : URL 뒤에 물음표를 붙여 key=value로 전달 예) google.com?q=북극곰
       
 @app.route('/test', methods=['GET'])
def test_get():
   title_receive = request.args.get('title_give')
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})
 (콘솔창)  
 $.ajax({
    type: "GET",
    url: "/test?title_give=봄날은간다",
    data: {},
    success: function(response){
       console.log(response)
    }
  })

 * POST: 통상적으로! 데이터 생성(Create), 변경(Update), 삭제(Delete) 요청 할 때 예) 회원가입, 회원탈퇴, 비밀번호 수정
       →  데이터 전달 : 바로 보이지 않는 HTML body에 key:value 형태로 전달
       
 @app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})
 (콘솔창)  
 $.ajax({
    type: "POST",
    url: "/test",
    data: { title_give:'봄날은간다' },
    success: function(response){
       console.log(response)
    }
  })
  
  주의사항
  request.args.get('변수')의 변수 = request.form['변수']의 변수
  
  
