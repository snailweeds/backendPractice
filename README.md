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
***
# BookReview
> Post: API 만들고 사용하기(정보 저장하기) --> Create=>Post
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

> Get: API 만들고 사용하기(정보 화면에 보여주기) --> Read=>Get
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
* 주의사항
```
다 사용한 파일들은 즉시 지워주기
window.location.reload() 코드로 새로고침 해주기
``` 
***
# AloneMemo
> meta tag? URL만 입력했는데, 자동으로 불러와지는 부분
```
<head></head> 부분에 들어가는, 눈으로 보이는 것(body) 외에 사이트의 속성을 설명해주는 태그

og_image = soup.select_one('meta[property="og:image"]')
og_title = soup.select_one('meta[property="og:title"]')
og_description = soup.select_one('meta[property="og:description"]')

url_image = og_image['content']
url_title = og_title['content']
url_description = og_description['content']

print(url_image)
print(url_title)
print(url_description)
```
> Post: API 만들고 사용하기(정보 저장하기) --> Create=>Post
* 클라이언트/서버 확인
```
포스팅API  - 카드 생성 (Create) : 클라이언트에서 받은 url, comment를 이용해서 페이지 정보를 찾고 저장하기

[서버 코드 - `app.py`]
@app.route('/memo', methods=['POST'])
def post_articles():
		sample_receive = request.form['sample_give']
		print(sample_receive)
    return jsonify({'msg': 'POST 연결되었습니다!'})
    
[클라이언트 코드 - `index.html`]
function postArticle() {
  $.ajax({
    type: "POST",
    url: "/memo",
    data: {sample_give:'샘플데이터'},
    success: function (response) { // 성공하면
      alert(response['msg']);
    }
  })
}

<button type="button" class="btn btn-primary" onclick="postArticle()">기사저장</button>
```
* 서버 만들기
```
1. 클라이언트로부터 데이터를 받기.
2. meta tag를 스크래핑하기
3. mongoDB에 데이터를 넣기

[서버 코드 - `app.py`]
@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'url':url_receive,
        'comment':comment_receive
    }

    db.articles.insert_one(doc)

    return jsonify({'msg':'저장이 완료되었습니다!'})
```
* 클라이언트 만들기
```
1. 유저가 입력한 데이터를 #post-url과 #post-comment에서 가져오기
2. /memo에 POST 방식으로 메모 생성 요청하기
3. 성공 시 페이지 새로고침하기

[클라이언트 코드 - `index.html`]
function postArticle() {
      let url = $('#post-url').val()
      let comment = $('#post-comment').val()

      $.ajax({
          type: "POST",
          url: "/memo",
          data: {url_give:url, comment_give:comment},
          success: function (response) { // 성공하면
              alert(response["msg"]);
              window.location.reload() // 새로고침
          }
      })
  }
```
* 완성/확인

> Get: API 만들고 사용하기(정보 화면에 보여주기) --> Read=>Get
* 클라이언트/서버 확인
```
리스팅API - 저장된 카드 보여주기 (Read)

[서버 코드 - `app.py`]
@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'msg':'GET 연결되었습니다!'})

[클라이언트 코드 - `index.html`]
function showArticles() {
  $.ajax({
    type: "GET",
    url: "/memo",
    data: {},
    success: function (response) {
      if (response["result"] == "success") {
        alert(response["msg"]);
      }
    }
  })
}
```
* 서버 만들기
```
1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
2. articles라는 키 값으로 articles 정보 보내주기

[서버 코드 - `app.py`]
@app.route('/memo', methods=['GET'])
def listing():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles':articles})
```
* 클라이언트 만들기
```
1. /memo에 GET 방식으로 메모 정보 요청하고 articles로 메모 정보 받기
2. , makeCard 함수를 이용해서 카드 HTML 붙이기

[클라이언트 코드 - `index.html`]
function showArticles() {
    $.ajax({
        type: "GET",
        url: "/memo",
        data: {},
        success: function (response) {
            let articles = response['all_articles']
            for (let i = 0; i < articles.length; i++) {
                let title = articles[i]['title']
                let image = articles[i]['image']
                let url = articles[i]['url']
                let desc = articles[i]['desc']
                let comment = articles[i]['comment']

                let temp_html = `<div class="card">
                                    <img class="card-img-top"
                                         src="${image}"
                                         alt="Card image cap">
                                    <div class="card-body">
                                        <a target="_blank" href="${url}" class="card-title">${title}</a>
                                        <p class="card-text">${desc}</p>
                                        <p class="card-text comment">${comment}</p>
                                    </div>
                                </div>`
                $('#cards-box').append(temp_html)
            }
        }
    })
}
```
* 완성/확인

# MovieStar
> DB 만들기 : 데이터 쌓기 (init_db.py)
1) 사용할 데이터를 웹 스크래핑해서, 2) 데이터베이스에 저장(insert_all())

> Get --> 보여주기:조회(Read) 기능
* 클라이언트/서버 확인
```
1. 요청 정보
- 요청 URL= /api/list , 요청 방식 = GET
- 요청 데이터 : 없음
2. 서버가 제공할 기능 :  데이터베이스에  영화인 정보를 조회(Read)하고, 영화인 정보를 응답 데이터로 보냄
3. 응답 데이터  : (JSON 형식) 'stars_list'= 영화인 정보 리스트

[서버 코드 - `app.py`]
@app.route('/api/list', methods=['GET'])
def show_stars():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'list 연결되었습니다!'})

[클라이언트 코드 - `index.html`]
function showStar() {
      $.ajax({
          type: 'GET',
          url: '/api/list?sample_give=샘플데이터',
          data: {},
          success: function (response) {
              alert(response['msg']);
          }
      });
  }
```
* 서버 만들기
```
1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬
2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달

[서버 코드 - `app.py`]
@app.route('/api/list', methods=['GET'])
def show_stars():
    movie_star = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'movie_stars': movie_star})
```
* 클라이언트 만들기
```
1. #star_box의 내부 html 태그를 모두 삭제
2. 서버에 1) GET 방식으로, 2) /api/list 라는 주소로 stars_list를 요청
3. 서버가 돌려준 stars_list를 stars라는 변수에 저장
4. for 문을 활용하여 stars 배열의 요소를 차례대로 조회
5. stars[i] 요소의 name, url, img_url, recent, like 키 값을 활용하여 값 조회
6. 영화인 카드 코드 만들어 #star-box에 붙이기

[클라이언트 코드 - `index.html`]
function showStar() {
                $.ajax({
                    type: 'GET',
                    url: '/api/list?sample_give=샘플데이터',
                    data: {},
                    success: function (response) {
                        let mystars = response['movie_stars']
                        for (let i = 0; i < mystars.length; i++) {
                            let name = mystars[i]['name']
                            let img_url = mystars[i]['img_url']
                            let recent = mystars[i]['recent']
                            let url = mystars[i]['url']
                            let like = mystars[i]['like']

                            let temp_html = `<div class="card">
                                                <div class="card-content">
                                                    <div class="media">
                                                        <div class="media-left">
                                                            <figure class="image is-48x48">
                                                                <img
                                                                        src="${img_url}"
                                                                        alt="Placeholder image"
                                                                />
                                                            </figure>
                                                        </div>
                                                        <div class="media-content">
                                                            <a href="${url}" target="_blank" class="star-name title is-4">${name} (좋아요: ${like})</a>
                                                            <p class="subtitle is-6">${recent}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                                <footer class="card-footer">
                                                    <a href="#" onclick="likeStar('${name}')" class="card-footer-item has-text-info">
                                                        위로!
                                                        <span class="icon">
                                              <i class="fas fa-thumbs-up"></i>
                                            </span>
                                                    </a>
                                                    <a href="#" onclick="deleteStar('${name}')" class="card-footer-item has-text-danger">
                                                        삭제
                                                        <span class="icon">
                                              <i class="fas fa-ban"></i>
                                            </span>
                                                    </a>
                                                </footer>
                                            </div>`
                            $('#star-box').append(temp_html)
                        }
                    }
                });
            }
```
* 완성/확인

> Post --> 좋아요: 클라이언트에서 받은 이름(name_give)으로 찾아서 좋아요(like)를 증가
* 클라이언트/서버 확인
```
[서버 코드 - `app.py`]
@app.route('/api/like', methods=['POST'])
def like_star():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'like 연결되었습니다!'})

[클라이언트 코드 - `index.html`]
function likeStar(name) {
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: {sample_give:'샘플데이터'},
        success: function (response) {
            alert(response['msg']);
        }
    });
}
```
* 서버 만들기
```
1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.

[서버 코드 - `app.py`]
@app.route('/api/like', methods=['POST'])
def like_star():
    name_receive = request.form['name_give']

    target_star = db.mystar.find_one({'name': name_receive})
    current_like = target_star['like']

    new_like = current_like + 1

    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})
```
* 클라이언트 만들기
```
1. 서버에 
  1) POST 방식으로, 
  2) /api/like 라는 url에, 
  3) name_give라는 이름으로 name을 전달합니다. 
  (참고) POST 방식이므로 data: {'name_give': name} 사용
2. '좋아요 완료!' alert 창을 띄웁니다.
3. 변경된 정보를 반영하기 위해 새로고침합니다.

[클라이언트 코드 - `index.html`]
function likeStar(name) {
    $.ajax({
        type: 'POST',
        url: '/api/like',
        data: {name_give:name},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}
```
> Post --> 삭제(Delete) 기능: 클라이언트에서 받은 이름(name_give)으로 영화인을 찾고, 해당 영화인을 삭제
* 클라이언트/서버 확인
```
[서버 코드 - `app.py`]
@app.route('/api/delete', methods=['POST'])
def delete_star():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'delete 연결되었습니다!'})

[클라이언트 코드 - `index.html`]
function deleteStar(name) {
    $.ajax({
        type: 'POST',
        url: '/api/delete',
        data: {sample_give:'샘플데이터'},
        success: function (response) {
            alert(response['msg']);
        }
    });
}
```
* 서버 만들기
```
1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣기
2. mystar 에서 delete_one으로 name이 name_receive와 일치하는 star를 제거
3. 성공하면 success 메시지를 반환

[서버 코드 - `app.py`]
@app.route('/api/delete', methods=['POST'])
def delete_star():
    name_receive = request.form['name_give']
    db.mystar.delete_one({'name': name_receive})
    return jsonify({'msg': '삭제 완료!'})
```
* 클라이언트 만들기
```
1. 서버에 
  1) POST 방식으로, 
  2) /api/delete 라는 url에, 
  3) name_give라는 이름으로 name을 전달
  (참고) POST 방식이므로 data: {'name_give': name} 
2. '삭제 완료! 안녕!' alert창 띄우기
3. 변경된 정보를 반영하기 위해 새로고침

[클라이언트 코드 - `index.html`]
function deleteStar(name) {
      $.ajax({
          type: 'POST',
          url: '/api/delete',
          data: {name_give:name},
          success: function (response) {
              alert(response['msg']);
              window.location.reload()
          }
      });
  }
```
* 완성/확인

* PyMongo 활용
```
정렬하여 가져오기: find().sort('value', 1은 ascending, 0은 descending)
```
