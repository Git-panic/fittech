from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from db_config import supabase
import json
from recommend import recommend_yoga_poses  # 요가 추천 모듈 불러오기
import logging
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
            
            data = request.json

            answerby = uid
            gender = data.get("gender")
            age = data.get("age")
            height = data.get("height")
            weight = data.get("weight")
            period = data.get('period')
            body_parts = json.dumps(ensure_list(data.get('body')))
            experience = json.dumps(ensure_list(data.get('experience')))
            week = data.get('week')
            purpose = json.dumps(ensure_list(data.get('purpose')))

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
    data = supabase.from_("answers").select("*").execute()

    survey_data = data.json()
    survey_data = json.loads(survey_data)

    print(survey_data["data"])

    with open('survey_data.json', 'w') as json_file:
        json.dump(survey_data['data'], json_file, indent=4)

    # 엑셀 파일에서 요가 데이터베이스 불러오기
    yoga_df = pd.read_excel("yoga_data.xlsx", engine='openpyxl')

    # 엑셀 파일의 첫 번째 열이 요가 동작의 이름이고, 나머지 열은 벡터 데이터입니다.
    # 예시 벡터 데이터가 숫자로 구성되어 있다고 가정하고, 해당 열을 NumPy 배열로 변환합니다.
    yoga_database = {row[0]: np.array(row[1:]) for row in yoga_df.values}

    # JSON 파일 읽기
    with open('survey_data.json', 'r', encoding='utf-8') as f:
        user_profiles = json.load(f)
        
    recommendations = recommend_yoga_poses(user_profiles, yoga_database)
    
    return render_template('showRecommend.html', recommendations=recommendations, session_id=session.get('id'))



# 사용자 프로필 벡터 생성 함수
def create_user_profile(user_data):
    experience_vector = np.zeros(3)  # 예: 경험 종류
    experiences = json.loads(user_data["experience"])
    experience_score = 0
    if 'offline' in experiences:
        experience_score += 2
    if 'online' in experiences:
        experience_score += 1
    if 'none' in experiences:
        experience_score += 0

    body_parts_vector = np.zeros(13)  # 주요 부위 13개
    body_part_indices = {
        "all": 0,
        "core": 1,
        "stomach": 2,
        "thigh": 3,
        "pelvis": 4,
        "leg": 5,
        "hip": 6,
        "back": 7,
        "waist": 8,
        "chest": 9,
        "neck": 10,
        "shoulder": 11,
        "arm": 12
    }
    body_parts = json.loads(user_data["body_parts"])
    for part in body_parts:
        if part in body_part_indices:
            body_parts_vector[body_part_indices[part]] = 1

    period_score = int(user_data["period"]) - 1
    week_score = int(user_data["week"]) - 1

    # difficulty_score 계산
    scores = [period_score, week_score, experience_score]
    difficulty_score = np.mean(scores)  # 평균 계산

    # difficulty_score를 0에서 3 사이로 정규화
    difficulty_score = (difficulty_score - min(scores)) / (max(scores) - min(scores)) * 3

    # 목적 벡터 생성
    purpose_vector = np.zeros(3)
    purposes = json.loads(user_data['purpose'])
    purpose_indices = {
        "strength": 0,       # 근력강화
        "flexibility": 1,    # 유연성 향상
        "stretching": 2      # 스트레칭
    }
    for purpose in purposes:
        if purpose in purpose_indices:
            purpose_vector[purpose_indices[purpose]] = 1

    user_vector = np.concatenate(([difficulty_score], body_parts_vector, purpose_vector))
    
    return user_vector

# 사용자 벡터 인덱스 이름 생성 함수
def create_user_vector_indices():
    indices = ["difficulty_score"]
    body_part_indices = [
        "all", "core", "stomach", "thigh", "pelvis",
        "leg", "hip", "back", "waist", "chest",
        "neck", "shoulder", "arm"
    ]
    indices += body_part_indices
    indices += ["purpose_strength", "purpose_flexibility", "purpose_stretching"]
    return indices

# 사용자 추천 요가 동작 함수
def recommend_yoga_poses(user_profiles, yoga_database):
    recommendations = []

    # 모든 사용자 벡터 생성 및 출력
    for user_data in user_profiles:
        user_profile = create_user_profile(user_data)
        
        # 코사인 유사도 계산
        similarities = {}
        for pose, vector in yoga_database.items():
            similarity = cosine_similarity([user_profile], [vector])[0][0]
            similarities[pose] = similarity

        # 유사도가 높은 순서대로 정렬
        sorted_poses = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        # 상위 N개의 요가 추천
        N = 3
        recommended_poses = [pose for pose, similarity in sorted_poses[:N]]

        recommendations.append({
            "answerby": user_data['answerby'],
            "user_id": user_data['id'],
            "recommended_poses": recommended_poses
        })

    return recommendations


def ensure_list(value):
    if isinstance(value, list):
        return value
    return [value]