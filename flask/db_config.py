from supabase import create_client

# Supabase URL과 Key 설정
supabase_url = "https://vldulsthmnzknlinmbqr.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZsZHVsc3RobW56a25saW5tYnFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyODY5NjUsImV4cCI6MjAyNzg2Mjk2NX0.Q5CQQrgoPWAUYHTycfQ40duZN5WW70LTJ_2lSM8UytM"

# Supabase 클라이언트 생성
supabase = create_client(supabase_url, supabase_key)

# Supabase 잘 연결 되었는지 코드

#response = supabase.from_("users").select("*").execute()
#print(response)