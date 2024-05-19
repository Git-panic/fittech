import json
from db_config import supabase


data = supabase.from_("answers").select("*").execute()

survey_data = data.json()
survey_data = json.loads(survey_data)

print(survey_data['data'])

with open('survey_data.json', 'w') as json_file:
    json.dump(survey_data['data'], json_file, indent=4)
