from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_config import supabase

log = Blueprint('log', __name__, template_folder="templates")

# 로그인 페이지
@log.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']

        # Supabase에서 사용자 정보 가져오기
        response = supabase.from_("users").select("user_id, user_password").eq("user_id", user_id).execute()
        user_record = response.data

        if user_record:
            stored_password = user_record[0]['user_password']
            if user_password == stored_password:
                # 비밀번호가 일치하는 경우
                session['user_id'] = user_id
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

        # Supabase에서 사용자 중복 확인
        response = supabase.from_("users").select("*").eq("user_id", user_id).execute()
        if response.data:
            flash("ID가 이미 존재합니다. 다른 ID를 선택해주세요.", 'error')
            return redirect(url_for('log.login'))

        # Supabase에 사용자 추가
        supabase.from_("users").insert({"user_name": user_name, "user_id": user_id, "user_password": user_password}).execute()

        session['user_id'] = user_id
        return redirect(url_for('home'))

    return render_template('register.html')

# 로그아웃
@log.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))
