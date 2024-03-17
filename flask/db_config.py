# db_config.py
import pymysql

try:
    # MySQL 연결 설정
    db = pymysql.connect(
        host='admin.cdha8hslaur6.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='root',
        passwd='root1234',
        db='users',
        charset='utf8'
    )
    
    # DB 연결이 성공적으로 이루어졌을 때 메시지 출력
    print("DB 연결이 성공적으로 이루어졌습니다.")
except pymysql.Error as e:
    # DB 연결 실패한 경우 예외 처리
    print(f"DB 연결 실패: {e}")
