import requests
import json

muscle = ['biceps', 'chest', 'lats']
# muscle  = 'biceps'
difficulty = 'expert'
exercise_type = 'stretching'
params={"difficulty":difficulty, "muscle": muscle, "type": exercise_type}
params.pop("type")
params.pop("muscle")
print(params)
params["offset"] = 0
count = 10
out = []
while count == 10:
    api_url = 'https://api.api-ninjas.com/v1/exercises'
    response = requests.get(api_url, headers={'X-Api-Key': 'l+gXOqDpMXvFh5QBU1ELfA==7NBqTRdwYgWp7OWP'},
    params=params)
    if response.status_code == requests.codes.ok:
        print(response.url)
        data = response.json()
        count = len(data)
        out += data
        params["offset"] += count
        print(count)
    else:
        count = 0
        print("Error:", response.status_code, response.text)
with open('output.json','w') as f:
    json.dump(out,f,indent=2)