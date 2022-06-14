# 4주 회고록

* Flask 프레임워크: 서버를 구동시켜주는 편한 코드 모음, 서버를 구동하려면 필요한 복잡한 일들을 쉽게 가져다 쓸 수 O
```
from flask import Flask --> 남들도 볼 수 있는 서버
app = Flask(__name__)

@app.route('/')  --> 서버 주소 뒤에 붙이는 것
def home():
   return 'This is Home!'  --> 출력되는 것 

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True) --> localhost:5000을 입력하면 'This is Home!' 출력됨

종료: 터미널 창을 클릭하시고, ctrl + c(ctrl + F2) 을 누르기
```
```
기본폴더구조(항상 이렇게 세팅) : 프로젝트 폴더 안에, (new>directory)
 ㄴstatic 폴더 (이미지, css파일을 넣어둡니다)
 ㄴtemplates 폴더 (html파일을 넣어둡니다)
 ㄴapp.py 파일
```
* render_template --> html 파일을 활용해 서버 열기
```
 import render_template
 return render_template('index.html')
 주의사항
 html파일 명 index.html로 통일
```
* GET: 통상적으로! 데이터 조회(Read)를 요청할 때 예) 영화 목록 조회
* 데이터 전달 : URL 뒤에 물음표를 붙여 key=value로 전달 예) google.com?q=북극곰
 ```      
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
```
 * POST: 통상적으로! 데이터 생성(Create), 변경(Update), 삭제(Delete) 요청 할 때 예) 회원가입, 회원탈퇴, 비밀번호 수정
 * 데이터 전달 : 바로 보이지 않는 HTML body에 key:value 형태로 전달
```      
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
```  
* 주의사항
```
통상적으로 flask 서버를 돌리는 파일은 app.py라고 이름 짓기!
request.args.get('변수')의 변수 = request.form['변수']의 변수
```  
  

# Post: API 만들고 사용하기(정보 저장하기) --> Create=>Post
* 클라이언트/서버 확인
```
1. 요청 정보 :  요청 URL= /review , 요청 방식 = POST
2. 서버가 제공할 기능 :  클라이언트에게 정해진 메시지를 보냄
3. 응답 데이터  : (JSON 형식) 'result'= 'success',  'msg'= '리뷰가 성공적으로 작성되었습니다.'

[서버 코드 - `app.py`]
API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
	# 1. 클라이언트가 준 title, author, review 가져오기.
	# 2. DB에 정보 삽입하기
	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})

[클라이언트 코드 - `index.html`]
function makeReview() {
		// 1. 제목, 저자, 리뷰 내용을 가져옵니다.
		// 2. 제목, 저자, 리뷰 중 하나라도 입력하지 않았을 경우 alert를 띄웁니다.
		// 3. POST /review 에 저장을 요청합니다.
    $.ajax({
        type: "POST",
        url:  "/review",
        data: { },
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"] );
                window.location.reload();
            }
        }
    })
}
```
* 서버 만들기
```
1. 클라이언트가 준 title, author, review 가져오기.
2. DB에 정보 삽입하기
3. 성공 여부 & 성공 메시지 반환하기

A. 요청 정보
- 요청 URL= /review , 요청 방식 = POST 
- 요청 데이터 : 제목(title), 저자(author), 리뷰(review)
B. 서버가 제공할 기능 :  클라이언트에게 보낸 요청 데이터를 데이터베이스에 생성(Create)하고, 저장이 성공했다고 응답 데이터를 보냄
C. 응답 데이터  : (JSON 형식) 'msg'= '리뷰가 성공적으로 작성되었습니다.'

[서버 코드 - `app.py`]
@app.route('/review', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    title_receive = request.form['title_give']
    # author_receive로 클라이언트가 준 author 가져오기
    author_receive = request.form['author_give']
    # review_receive로 클라이언트가 준 review 가져오기
    review_receive = request.form['review_give']

    # DB에 삽입할 review 만들기
    doc = {
        'title': title_receive,
        'author': author_receive,
        'review': review_receive
    }
    # reviews에 review 저장하기
    db.bookreview.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'msg': '리뷰가 성공적으로 작성되었습니다.'})
```
* 클라이언트 만들기
```
1. input에서 title, author, review 가져오기
2. 입력값이 하나라도 없을 때 alert 띄우기.
3. Ajax로 서버에 저장 요청하고, 화면 다시 로딩하기

A. 요청 정보
- 요청 URL= /review , 요청 방식 = POST 
- 요청 데이터 : 제목(title), 저자(author), 리뷰(review)
B. 서버가 제공할 기능 :  클라이언트에게 보낸 요청 데이터를 데이터베이스에 생성(Create)하고, 저장이 성공했다고 응답 데이터를 보냄
C. 응답 데이터  : (JSON 형식) 'result'= 'success',  'msg'= '리뷰가 성공적으로 작성되었습니다.'

[클라이언트 코드 - `index.html`]
function makeReview() {
    // 화면에 입력어 있는 제목, 저자, 리뷰 내용을 가져옵니다.
    let title = $("#title").val();
    let author = $("#author").val();
    let review = $("#bookReview").val();

    // POST /review 에 저장(Create)을 요청합니다.
    $.ajax({
        type: "POST",
        url: "/review",
        data: { title_give: title, author_give: author, review_give: review },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    })
}
```
* 완성/확인

# Get: API 만들고 사용하기(정보 화면에 보여주기) --> Read=>Get
* 클라이언트/서버 확인
```
1. 요청 정보 :  요청 URL= /review , 요청 방식 = GET
2. 서버가 제공할 기능 :  클라이언트에게 정해진 메시지를 보냄
3. 응답 데이터  : (JSON 형식) {'msg': '이 요청은 GET!'}

[서버 코드 - `app.py`]
@app.route('/review', methods=['GET'])
def read_reviews():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': '이 요청은 GET!'})

[클라이언트 코드 - `index.html`]
function showReview() {
		// 서버의 데이터를 받아오기
		$.ajax({
        type: "GET",
        url: "/review?sample_give=샘플데이터",
        data: {},
        success: function (response) {
            alert(response["msg"]);
        }
    })
}
```
* 서버 만들기
```
1. DB에서 리뷰 정보 모두 가져오기
2. 성공 여부 & 리뷰 목록 반환하기

A. 요청 정보
- 요청 URL= /review , 요청 방식 = GET 
- 요청 데이터 : 없음
B. 서버가 제공할 기능 :  데이터베이스에 리뷰 정보를 조회(Read)하고, 성공 메시지와 리뷰 정보를 응답 데이터를 보냄
C. 응답 데이터  : (JSON 형식) 'all_reviews'= 리뷰리스트

[서버 코드 - `app.py`]
@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.bookreview.find({}, {'_id': False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'all_reviews': reviews})
```
* 클라이언트 만들기
```
1. 리뷰 목록을 서버에 요청하기
2. 요청 성공 여부 확인하기
3. 요청 성공했을 때 리뷰를 올바르게 화면에 나타내기

A. 요청 정보
- 요청 URL= /review , 요청 방식 = GET 
- 요청 데이터 : 없음
B. 서버가 제공할 기능 :  데이터베이스에 리뷰 정보를 조회(Read)하고, 성공 메시지와 리뷰 정보를 응답 데이터를 보냄
C. 응답 데이터  : (JSON 형식) 'all_reviews'= 리뷰리스트

[클라이언트 코드 - `index.html`]
function showReview() {
                $.ajax({
                    type: "GET",
                    url: "/review",
                    data: {},
                    success: function (response) {
                        let reviews = response['all_reviews']
                        for (let i = 0; i < reviews.length; i++) {
                            let title = reviews[i]['title']
                            let author = reviews[i]['author']
                            let review = reviews[i]['review']

                            let temp_html = `<tr>
                                                <td>${title}</td>
                                                <td>${author}</td>
                                                <td>${review}</td>
                                            </tr>`
                            $('#reviews-box').append(temp_html)
                        }
                    }
                })
            }
```
* 완성/확인


