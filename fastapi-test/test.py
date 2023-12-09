import requests
import json

muscle = 'biceps'
difficulty = 'beginner'
exercise_type = 'stretching'
params={"difficulty":difficulty, "muscle": muscle, "type": exercise_type}
api_url = 'https://api.api-ninjas.com/v1/exercises?muscle=chest,biceps'
response = requests.get(api_url, headers={'X-Api-Key': 'l+gXOqDpMXvFh5QBU1ELfA==7NBqTRdwYgWp7OWP'},
params={"difficulty":difficulty, "muscle": muscle, "type": exercise_type})
if response.status_code == requests.codes.ok:
    data = response.json()
    with open('output.json','w') as f:
        json.dump(data,f,indent=2)
else:
    print("Error:", response.status_code, response.text)