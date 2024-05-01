from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_config import supabase
import json


sur = Blueprint('sur', __name__, template_folder="templates")

@sur.route('/survey')
def survey():
    return render_template('survey.html')

# 설문조사 페이지
@sur.route('/survey_answer', methods=['GET', 'POST'])
def survey_answer():
    if request.method == 'POST':
        # 현재 로그인된 사용자의 users table 가져오기
        user_id = session['user_id']
        current_user = supabase.from_("users").select("*").eq("user_id",user_id).execute()
        print(current_user)

        response_data = current_user.json()
        response_data = json.loads(response_data)

        print(response_data)

        # 데이터에서 원하는 정보 추출
        uid = response_data['data'][0]['id']


        # 폼에서 사용자 입력 받기
        answerby = uid
        gender = request.form['gender']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        period = request.form['period']
        body_parts = request.form.getlist('body')
        experience = request.form.getlist('experience')
        week = request.form['week']
        purpose = request.form.getlist('purpose')
        
        try:
            # Supabase에 데이터 저장
            response = supabase.from_("answers").insert({
                "answerby" : answerby,
                "gender": gender,
                "age" : age,
                "height" : height,
                "weight" : weight,
                "period" : period,
                "body_parts" : body_parts,
                "experience" : experience,
                "week" : week,
                "purpose" : purpose,
            }).execute()
            
            # 데이터가 성공적으로 저장되었는지 확인
            if response.get("error") is None:
                flash("설문이 성공적으로 제출되었습니다. 감사합니다!", "success")
                return redirect(url_for('mypage'))  # 설문 완료 후 홈 페이지로 이동
            else:
                flash("설문을 제출하는 중 문제가 발생했습니다. 나중에 다시 시도해주세요.", "error")
                return redirect(url_for('sur.survey_answer'))  # 문제 발생 시 다시 설문 페이지로 이동

        except Exception as e:
            flash("설문을 제출하는 중 문제가 발생했습니다. 나중에 다시 시도해주세요.", "error")
            return redirect(url_for('sur.survey_answer'))  # 문제 발생 시 다시 설문 페이지로 이동


    return render_template('mypage.html')
