from flask import Blueprint, render_template, request, redirect, url_for, session, flash

log = Blueprint('log', __name__, template_folder="templates")
from db_config import db  # db_config 모듈에서 db 불러오기


# 로그인 페이지
@log.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']

        cursor = db.cursor()
        cursor.execute("SELECT user_name, user_password FROM users2 WHERE user_id = %s", (user_id,))
        user_record = cursor.fetchone()
        cursor.close()

        if user_record:
            stored_password = user_record[1]
            if user_password == stored_password:
                # 비밀번호가 일치하는 경우
                session['user_id'] = user_id
                session['user_name'] = user_record[0]  # user_name을 세션에 저장
                return redirect(url_for('home'))

        # 비밀번호가 일치하지 않는 경우
        flash("Email이나 Password가 일치하지 않습니다.", "error")
        return redirect(url_for('log.login'))

    return render_template('login.html')

# 회원가입 페이지
@log.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼 데이터에서 정보 검색
        user_name = request.form['user_name']
        user_id = request.form['user_id']
        user_password = request.form['user_password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users2 WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            flash("ID가 이미 존재합니다. 다른 ID를 선택해주세요.", 'error')
            return redirect(url_for('log.login'))

        cursor.execute("INSERT INTO users2 (user_name, user_id, user_password) VALUES (%s, %s, %s)",
                       (user_name, user_id, user_password))
        db.commit()
        cursor.close()

        session['user_id'] = user_id
        session['user_name'] = user_name

        return redirect(url_for('home'))

    return render_template('register.html')

# 로그아웃
@log.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))
