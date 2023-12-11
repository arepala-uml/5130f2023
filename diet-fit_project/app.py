from async_requests import AsyncBaseApi
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import time
import json
import os
import sys
import bcrypt
import uvicorn
from pymongo import MongoClient, ASCENDING
from pydantic import BaseModel

class UserSignup(BaseModel):
    firstName: str 
    lastName: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

async_base_api = AsyncBaseApi()
mongo_password = os.getenv("MONGO_PASSWORD", "")
if mongo_password == "":
    print("unable to get mongoDB password from os, so exiting...")
    sys.exit(1)
MONGO_URI = f"mongodb+srv://5130f2023:{mongo_password}@5130f2023-iws.kprx95f.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "dietfit"
USERS_COLLECTION = "users"
EXERCISE_COLLECTION = "exercises"

async def startup_aiohttp() -> None:
    async_base_api.get_aiohttp_client()

async def shutdown_aiohttp() -> None:
    await async_base_api.close_aiohttp_client()

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

# Initialize MongoDB client
def get_db():
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        print("got successful connection to MongoDB!")
        return client[DB_NAME]
    except Exception as e:
        print("error while connecting to MongoDB - %s"%(e))
        sys.exit(1)

def create_indexes(collection, indexes):
    final_indexes = []
    for index in indexes:
        final_indexes.append((index, ASCENDING))
    collection.create_index(final_indexes, unique=True)
    return collection

def get_users_collection(db):
    users_collection = db[USERS_COLLECTION]
    actual_indexes = ["email"]
    return create_indexes(users_collection, actual_indexes)

def get_exercises_collection(db):
    exercises_collection = db[EXERCISE_COLLECTION]
    actual_indexes = ['name', 'type', 'muscle', 'equipment', 'difficulty']
    return create_indexes(exercises_collection, actual_indexes)

db = get_db()
users_collection = get_users_collection(db)
exercises_collection = get_exercises_collection(db)

# user collection utility functions
def get_user(email):
    return users_collection.find_one({'email': email})

def create_user(new_user):
    users_collection.insert_one(new_user)

# user password utiliy functions
def get_hashed_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def match_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)

APP_NAME = "fastapi-server"
APP_DESCRIPTION = "fastapi server for dietfit"
API_RELEASE_VERSION = "1.0.0"
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=API_RELEASE_VERSION,
    docs_url="/docs",
    on_startup=[startup_aiohttp],
    on_shutdown=[shutdown_aiohttp],
    debug=False
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/simple")
async def simple_get():
    url = "http://localhost:3000/data"
    response = await async_base_api.get(url=url)
    return response

@app.post("/viewDiet")
async def multi_get(request: Request):
    result={}
    t1 = time.time()
    post_body = await request.json()


    isValid = validateJSON(json.dumps(post_body))
    print(isValid)
    print(post_body)
    # post_body = {
    #     "size": 2,
    #     "plan": {
    #         "accept": {
    #             "all": [
    #                 {
    #                     "health": [
    #                         "CELERY_FREE",
    #                         "FISH_FREE",
    #                         "SESAME_FREE"
    #                     ]
    #                 }
    #             ]
    #         },
    #         "fit": {
    #             "ENERC_KCAL": {
    #                 "min": 1000,
    #                 "max": 2000
    #             },
    #             "PROCNT": {
    #                 "min": 10
    #             }
    #         },
    #         "sections": {
    #             "Breakfast": {
    #                 "accept": {
    #                     "all": [
    #                         {
    #                             "dish": [
    #                                 "cereals",
    #                                 "pastry",
    #                                 "seafood"
    #                             ]
    #                         },
    #                         {
    #                             "meal": [
    #                                 "breakfast"
    #                             ]
    #                         }
    #                     ]
    #                 },
    #                 "fit": {
    #                     "ENERC_KCAL": {
    #                         "min": 100,
    #                         "max": 600
    #                     }
    #                 }
    #             },
    #             "Dinner": {
    #                 "accept": {
    #                     "all": [
    #                         {
    #                             "dish": [
    #                                 "pies and tarts",
    #                                 "soup",
    #                                 "salad",
    #                                 "main course"
    #                             ]
    #                         },
    #                         {
    #                             "meal": [
    #                                 "lunch/dinner"
    #                             ]
    #                         }
    #                     ]
    #                 },
    #                 "fit": {
    #                     "ENERC_KCAL": {
    #                         "min": 200,
    #                         "max": 900
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }
   
    # # post_body = await request.json()
    
    # post_body = {'size': 7, 'plan': {'accept': {'all': [{'health': ['CELERY_FREE', 'GLUTEN_FREE', 'HIGH_PROTEIN', 'LOW_FAT']}]}, 'fit': {'ENERC_KCAL': {'min': 1000, 'max': 2000}, 'PROCNT': {'min': 10}}, 'sections': {'Breakfast': {'accept': {'all': [{'dish': ['main course', 'pies and tarts']}, {'meal': ['breakfast']}]}, 'fit': {'ENERC_KCAL': {'min': 150, 'max': 300}}}, 'Lunch': {'accept': {'all': [{'dish': ['ice cream and custard', 'pancake']}, {'meal': ['lunch/dinner']}]}, 'fit': {'ENERC_KCAL': {'min': 150, 'max': 600}}}, 'Dinner': {'accept': {'all': [{'dish': ['pastry', 'salad']}, {'meal': ['lunch/dinner']}]}, 'fit': {'ENERC_KCAL': {'min': 150, 'max': 600}}}}}}
    # print(post_body)
    # post_body = {    "size": 7,    "plan": {        "accept": {            "all": [               {"health": [ "DAIRY_FREE", "MUSTARD_FREE"]},{"diet": [ "BALANCED"]}            ]        },        "fit": {            "ENERC_KCAL": {"min": 1000, "max": 2000},"PROCNT": {"min": 10}        },        "sections": {            "Breakfast": {   "accept": {       "all": [           {"dish": ["bread","cereals","egg"]},{"meal": [ "breakfast" ]}       ]   },   "fit": {       "ENERC_KCAL": {"min": 100, "max": 600}   }},"Lunch": {   "accept": {       "all": [           {"dish": ["salad","sandwiches","side dish"]},{"meal": [ "lunch/dinner" ]}       ]   },   "fit": {       "ENERC_KCAL": {"min": 300, "max": 900}   }},"Dinner": {   "accept": {       "all": [          {"dish": ["seafood","soup"]},{"meal": [ "lunch/dinner" ]}       ]   },   "fit": {       "ENERC_KCAL": {"min": 200, "max": 900}   }}        }    }}
    # edamam dev keys


    

    # JithendraKoleti
    post_app_id = "df73a8c7"
    post_app_key = "2413b205b880ef489929e5af3f47465d"
    get_app_id = "df73a8c7"
    get_app_key = "2413b205b880ef489929e5af3f47465d"

    # edamam app
    # post_app_id = "b26fb46d"
    # post_app_key = "c887a724df8435d92a76f3ec8b3ba91a"
    # get_app_id = "469fc797"
    # get_app_key = "01c8217e070a97ba8180863e94daa8e6"
    post_url = f"https://api.edamam.com/api/meal-planner/v1/{str(post_app_id)}/select"
    post_params = {
        "app_id": post_app_id,
        "app_key": post_app_key
    }
    
    post_resp = await async_base_api.post(url=post_url, body=json.dumps(post_body), params=post_params)
    if post_resp["status_code"] == 200:
        resp = json.loads(post_resp['body'])
        if resp["status"] == "OK":
            recipe_urls = {
                "Breakfast": [],
                "Lunch": [],
                "Dinner": []
            }
            for selection_list in resp["selection"]:
                for meal, assigned_obj in selection_list["sections"].items():
                    if assigned_obj["assigned"]:
                        recipe_urls[meal].append(str(assigned_obj["assigned"]).split("#")[1])
            get_resp_map = {}
            get_url = f"https://api.edamam.com/api/recipes/v2/RECIPE?type=public&app_id={get_app_id}&app_key={get_app_key}"
            #print(recipe_urls)
            for meal in recipe_urls:
                for recipe_id in recipe_urls[meal]:
                    string = meal + "::" + recipe_id
                    get_resp_map[string] = await async_base_api.get(get_url.replace("RECIPE", recipe_id))
                    

            for i in range(1,8):
                day="Day_%i" %(i)
                result[day]={}
            print(result)
            bc=1
            lc=1
            dc=1
            for key in  get_resp_map:
                # print("*"*70)
                print(key)
                data={}
                response_data= get_resp_map[key]
                recipe_data=json.loads(response_data["body"])["recipe"]
                #print(recipe_data)
                data["name"]=recipe_data["label"]
                data["image"]=recipe_data["images"]["THUMBNAIL"]["url"]
                data["servings"]=recipe_data["yield"]
                calories=(recipe_data["totalNutrients"]["ENERC_KCAL"]["quantity"])/recipe_data["yield"]
                protein=(recipe_data["totalNutrients"]["PROCNT"]["quantity"])/recipe_data["yield"]
                carbs=(recipe_data["totalNutrients"]["CHOCDF"]["quantity"])/recipe_data["yield"]
                fat=(recipe_data["totalNutrients"]["FAT"]["quantity"])/recipe_data["yield"]
                data["calories"]= "%i %s" %(calories,recipe_data["totalNutrients"]["ENERC_KCAL"]["unit"]) 
                data["protein"]= "%i %s" %(protein,recipe_data["totalNutrients"]["PROCNT"]["unit"])
                data["carbs"]= "%i %s" %(carbs,recipe_data["totalNutrients"]["CHOCDF"]["unit"])
                data["fat"]= "%i %s" %(fat,recipe_data["totalNutrients"]["FAT"]["unit"])
                data["source"]=recipe_data["source"]
                data["url"]=recipe_data["url"]
                data["instructions"]=recipe_data["ingredientLines"]
                print(data)
                if "Breakfast" in key:
                    meal_type="Breakfast"
                    day="Day_%i" %(bc)
                    result[day][meal_type]=data
                    bc= bc+1
                elif "Lunch" in key:
                    meal_type="Lunch"
                    day="Day_%i" %(lc)
                    result[day][meal_type]=data
                    lc = lc+1
                else:
                    meal_type="Dinner"
                    day="Day_%i" %(dc)
                    result[day][meal_type]=data
                    dc = dc+1
            print(result)

        else:
            print("status not OK")
    else:
        print("post request failed - %s"%(post_resp['error']))
        return JSONResponse(content={"success": False,"data":result,"error":post_resp['error']}, status_code=401)
    t2 = time.time()
    print(t2-t1)
    print(post_resp)
    return JSONResponse(content={"success": True,"data":result,"error":""}, status_code=200)

@app.get('/', response_class=HTMLResponse)
def default_route(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/home', response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/about', response_class=HTMLResponse)
def user_details(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request": request})

@app.get('/signup', response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/logout', response_class=HTMLResponse)
def logout_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/bmi', response_class=HTMLResponse)
def bmi_page(request: Request):
    return templates.TemplateResponse("bmi.html", {"request": request})

@app.get('/dietplan', response_class=HTMLResponse)
def dietplan_page(request: Request):
    return templates.TemplateResponse("dietplan.html", {"request": request})

@app.get('/exerciseplan', response_class=HTMLResponse)
def exerciseplan_page(request: Request):
    return templates.TemplateResponse("exerciseplan.html", {"request": request})

# @app.get('/userdetails/dietplan', methods=['GET'])
# def dietplan_details():
#     # Pass user data as query parameters to the 'dietplan.html' page
#     user_data = {
#         'age': request.args.get('age'),
#         'height': request.args.get('height'),
#         'weight': request.args.get('weight'),
#         'gender': request.args.get('gender')
#     }
#     return render_template('dietplan.html', user_data=user_data)

@app.post('/signupCheck')
async def signup(user: UserSignup):
    email = user.email
    password = user.password
    firstName = user.firstName
    lastName = user.lastName
    user_data = get_user(email)
    if user_data:
        return JSONResponse(content={"success": False, "message": "User already exists"}, status_code=401)
    new_user = {
        "email": email,
        "firstName": firstName,
        "lastName": lastName,
        "password": get_hashed_password(password)
    }
    create_user(new_user)
    print("successfully inserted new user in mongodb")
    return JSONResponse(content={"success": True, "message": "User signup is successful"}, status_code=200)

@app.post('/loginCheck')
async def login(user: UserLogin):
    email = user.email
    password = user.password
    print(email, password)
    user_data = get_user(email)
    if user_data:
        if match_password(password, user_data['password']):
            return JSONResponse(content={"success": True, "message": "login successful"}, status_code=200)
        else:
            print("incorrect password")
            return JSONResponse(content={"success": False, "message": "incorrect password"}, status_code=401)
    else:
        print("user details not found, try signing up")
        return JSONResponse(content={"success": False,"message": "user details not found, try signing up"}, status_code=401)

@app.post('/getFirstname')
async def getFirstname(request: Request):
    request_data = await request.json()
    email = request_data.get('email', None)
    if email:
        user_data = get_user(email)
        if user_data:
            return JSONResponse(content={"firstName": user_data["firstName"],"success": True},status_code=200)
        else:
            return JSONResponse(content={"firstName": "User not found","success": False},status_code=401)
    else:
        return JSONResponse(content={"firstName": "Email not provided in the request","success": False},status_code=401)

@app.post('/calculate_bmi')
async def calculate_bmi(request: Request):
    data = await request.json()
    gender = data.get('gender',None)
    age = data.get('age',None)
    height = int(data.get('height',None))
    weight = int(data.get('weight',None))

    bmi = weight / ((height / 100) ** 2)
    return JSONResponse(content={"bmi": bmi,"success": True},status_code=200)

@app.post('/calculate_calories')
async def calculate_calories(request: Request):
    data = await request.json()
    gender = data.get('gender',None)
    age = data.get('age',None)
    height = int(data.get('height',None))
    weight = int(data.get('weight',None))
    bmi = weight / ((height / 100) ** 2)

    # Define calorie intake based on gender and BMI
    calorie_intake = 2000
    if gender == 'male':
        if bmi < 18.5:
            calorie_intake = 2500  
        elif 18.5 <= bmi < 24.9:
            calorie_intake = 2200
        else:
            calorie_intake = 2000
    elif gender == 'female':
        if bmi < 18.5:
            calorie_intake = 2000
        elif 18.5 <= bmi < 24.9:
            calorie_intake = 1800
        else:
            calorie_intake = 1600
    print(calorie_intake)    
    return JSONResponse(content={"calorie_intake": calorie_intake,"success": True},status_code=200)

@app.get("/test_route")
async def multi_get(req: Request):
    print(req)
    # print(await req.body())
    # print(await req.json())
    print(req.query_params.items())
    print(req.get('name'))
    return {}

@app.post("/test_route_post")
async def multi_get(req: Request):
    body = await req.body()
    print(body)
    return json.loads(body)

def push_exercise_data_to_mongo():
    for file in ['beginner.json', 'intermediate.json', 'expert.json']:
        with open(file, 'r') as fin:
            collection_name = file.split('.')[0]
            data = json.load(fin)
            push_data = []
            for workout in data:
                if workout['instructions'] != "":
                    push_data.append(workout)
            for obj in push_data:
                print(obj['difficulty'], obj['name'])
                try:
                    exercises_collection.insert_one(obj)
                except Exception as e:
                    if 'DuplicateKeyError' in str(e):
                        print("data dupe found for %s"%(obj['name']))

@app.post("/getExercises")
async def get_exercises(request: Request):
    try:
        query_params = await request.json()
        db_resp = exercises_collection.find({"$and": [
            { "difficulty": query_params["difficulty"] },
            { "type": { "$in": query_params["type"]} },
            { "muscle": { "$in": query_params["muscle"]} }
        ]}, { "_id": 0 })
        data_by_muscle = {}
        for doc in db_resp:
            muscle = doc["muscle"]
            if not data_by_muscle.get(muscle):
                data_by_muscle[muscle] = []
            data_by_muscle[muscle].append(doc)
        for muscle in data_by_muscle:
            while len(data_by_muscle[muscle]) <= 21:
                data_by_muscle[muscle] += data_by_muscle[muscle]
        muscle_exercise_count_map = {}
        resp = []
        while len(resp) != 7:
            for muscle in data_by_muscle:
                if not muscle_exercise_count_map.get(muscle):
                    muscle_exercise_count_map[muscle] = 0
                last_count = muscle_exercise_count_map[muscle]
                day_data = data_by_muscle[muscle][last_count:last_count+3]
                muscle_exercise_count_map[muscle] += 3
                resp.append(day_data)
            if len(resp) >= 7:
                break
        resp_obj = {}
        for i in range(7):
            resp_obj["Day_%d"%(i+1)] = resp[i]
        return JSONResponse(content={"exercise_data": resp_obj,"success": True},status_code=200)
    except Exception as e:
        raise JSONResponse(content={"message": "error while fetching exercise data from mongoDB","success": False, "error": str(e)},status_code=401)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, 
                reload=True, log_level="debug")