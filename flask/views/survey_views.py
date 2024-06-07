from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from db_config import supabase
import json
from recommend import recommend_yoga_poses  # 요가 추천 모듈 불러오기
import logging

logging.basicConfig(level=logging.DEBUG)

sur = Blueprint('sur', __name__, template_folder="templates")

@sur.route('/survey')
def survey():
    return render_template('survey.html')

# 설문조사 페이지
@sur.route('/survey_answer', methods=['POST'])
def survey_answer():
    try:
        if request.method == 'POST':
            user_id = session.get('user_id')
            if not user_id:
                logging.error("로그인 필요: 세션에 user_id 없음")
                return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401

            logging.debug(f"user_id: {user_id}")

            current_user_response = supabase.from_("users").select("*").eq("user_id", user_id).execute()
            logging.debug(f"current_user_response: {current_user_response}")

            current_user = current_user_response.data
            logging.debug(f"current_user: {current_user}")

            uid = current_user[0]["id"]
            logging.debug(f"사용자 ID: {uid}")

            answerby = uid
            gender = request.json.get('gender')
            age = request.json.get('age')
            height = request.json.get('height')
            weight = request.json.get('weight')
            period = request.json.get('period')
            body_parts = request.json.get('body')
            experience = request.json.get('experience')
            week = request.json.get('week')
            purpose = request.json.get('purpose')

            logging.debug(f"Received data: {request.json}")
            
            aresponse = supabase.from_("answers").select('*').eq('answerby', uid).execute()
            if aresponse.data:
                response = supabase.from_("answers").update({
                    "answerby" : answerby,
                    "gender": gender,
                    "age" : age,
                    "height" : height,
                    "weight" : weight,
                    "period" : period,
                    "body_parts" : body_parts,
                    "experience" : experience,
                    "week" : week,
                    "purpose" : purpose,}).match({'answerby': uid}).execute()
                
            else:
                response = supabase.from_("answers").insert({
                    "answerby": answerby,
                    "gender": gender,
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "period": period,
                    "body_parts": body_parts,
                    "experience": experience,
                    "week": week,
                    "purpose": purpose,
                }).execute()


            logging.debug(f"Supabase response: {response}")

            if response.data:
                return jsonify({"success": True, "message": "설문이 성공적으로 제출되었습니다. 감사합니다!"})
            else:
                logging.error(f"Supabase insert error: {response.error}")
                return jsonify({"success": False, "message": "설문을 제출하는 중 문제가 발생했습니다. 나중에 다시 시도해주세요."}), 500

    except Exception as e:
        logging.error(f"Exception during survey submission: {str(e)}")
        return jsonify({"success": False, "message": f"설문을 제출하는 중 문제가 발생했습니다: {str(e)}"}), 500

    logging.error("잘못된 요청")
    return jsonify({"success": False, "message": "잘못된 요청입니다."}), 400

@sur.route('/recommend')
def recommend():
    recommendations = recommend_yoga_poses()
    return render_template('showRecommend.html', recommendations=recommendations, session_id=session['id'])