from flask import *
import uuid

app = Flask(__name__)



###### 세션 생성 함수 ######
def create_session(value):

    session_id = str(uuid.uuid4())
    # uuid를 이용한 고유한 세션ID 생성
    session_store[session_id] = value  
    # key: 세션 ID | value: login_id(memberA) 을 세션 저장소에 저장

    return session_id
###### 세션 생성 함수 ######

# 회원 저장소 #
user_store = {
    "user" : "password",
    "sumi" : "sumi123"
}

# 세션저장소 #
session_store = {}

# 로그인 성공 함수 #
def success_login(login_id, password):
    return user_store.get(login_id) == password

#### 로그인 #### ### 쿠키 생성 ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['username']
        password = request.form['password']
        #로그인 값 가져옴#
        
        if success_login(login_id, password): # 로그인 성공할 경우

            ##login_id를 value값으로 세션ID 생성
            session_id = create_session(login_id)  

            # 응답을 만들어서 세션 ID를 쿠키(mySessionID)에 넣음
            response = make_response(redirect(url_for('home')))
            response.set_cookie("mySessionID", session_id) ## mySessionID == 쿠키
            return response
        else:
            # 로그인 실패 시 
            return render_template('login.html')
    return render_template('login.html')

# 홈 페이지
@app.route('/')
def home():
    session_id = request.cookies.get("mySessionID")
    # 쿠키(mySessionID)에서 생성한 세션 ID를 가져옴
    # mySessionID는 아까 만든 세션ID를 넣은 쿠키

    if session_id in session_store:
        # 세션 저장소에 세션 ID가 있으면
        login_id = session_store[session_id]
        # 세션 저장소에서 로그인 ID를 가져옴
        return render_template('home.html', user=login_id)
    

    # 로그인하지 않았다면 로그인 페이지로 리디렉션
    return redirect(url_for('login'))



# 로그아웃 시 세션 삭제 #
@app.route('/logout')
def logout():
    session_id = request.cookies.get("mySessionID")
    
    if session_id and session_id in session_store:
        # 세션 삭제
        del session_store[session_id]
    
    # 쿠키 삭제
    response = make_response(redirect(url_for('login')))
    response.set_cookie("mySessionID", '', expires=0)
    return response




# 세션 정보 확인 페이지 #
@app.route('/session_store')

def session_info():

    # 쿠키(mySessionID)에서 생성한 세션 ID를 가져옴
    session_id = request.cookies.get("mySessionID")

    # 세션 ID가 없거나 세션 저장소에 세션 ID가 없으면
    if not session_id or session_id not in session_store:
        return "세션이 없습니다."
    
    # 세션 저장소에서 사용자를 가져옴
    user = session_store[session_id]    
    ##   <세션 저장소의 구조> key : session_id, value : login_id(memberA)   ##
    session_data = {
        "session_id": session_id,
        "user": user
    }
    return session_data

if __name__ == '__main__':
    app.run()
