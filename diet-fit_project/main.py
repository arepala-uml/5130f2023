from flask import Flask, request, jsonify, redirect, url_for,render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dietfitdb'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# MongoDB Utility Functions
def get_user(username):
    return mongo.db.users.find_one({'username': username})


def create_user(username, password):
    mongo.db.users.insert({'username': username, 'password': password})


# User Class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user(user_id)
    if not user_data:
        return None
    return User(user_data['username'], user_data['password'])


# Routes for Authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_data = get_user(username)
    if user_data and user_data['password'] == password:
        user = User(username, password)
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# Protected Route Example
@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'This is a protected route for authenticated users', 'username': current_user.id})


# Your Existing Routes

# Default Route
@app.route('/', methods=['GET'])
def default_route():
    #print("default route")
    #response = {'hello': 'world'}
    return render_template('home.html')

@app.route('/home', methods=['GET'])
def home_page():
    #print("default route")
    #response = {'hello': 'world'}
    return render_template('home.html')

@app.route('/userdetails', methods=['GET'])
def user_details():
    #print("default route")
    #response = {'hello': 'world'}
    return render_template('userdetails.html')

@app.route('/userdetails/dietplan', methods=['GET'])
def dietplan_details():
    # Pass user data as query parameters to the 'dietplan.html' page
    user_data = {
        'age': request.args.get('age'),
        'height': request.args.get('height'),
        'weight': request.args.get('weight'),
        'gender': request.args.get('gender')
    }
    return render_template('dietplan.html', user_data=user_data)

@app.route('/login', methods=['GET'])
def login_page():
    #print("default route")
    #response = {'hello': 'world'}
    return render_template('login.html')

# Calculate BMI
@app.route('/calculate_bmi', methods=['POST', 'OPTIONS'])
def calculate_bmi():
    if request.method == 'OPTIONS':
        # Respond to the preflight OPTIONS request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    elif request.method == 'POST':
        # Handle the actual POST request
        data = request.get_json()
        gender = data.get('gender')
        age = data.get('age')
        height = int(data.get('height'))
        weight = int(data.get('weight'))

        # took this formula from - https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
        bmi = weight / ((height / 100) ** 2)

        response = {'bmi': bmi}
        print(response)
        return jsonify(response)


# Calculate Average Calorie Intake
@app.route('/calculate_calories', methods=['POST'])
def calculate_calories():
    if request.method == 'OPTIONS':
        # Respond to the preflight OPTIONS request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    elif request.method == 'POST':
        # Handle the actual POST request
        data = request.get_json()
        gender = data.get('gender')
        age = data.get('age')
        height = int(data.get('height'))
        weight = int(data.get('weight'))

        # took this formula from - https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
        bmi = weight / ((height / 100) ** 2)

        # Define calorie intake based on gender and BMI
        calorie_intake = 2000
        # TODO - Example value written for first week, adjustments with respect to few more parameters are needed
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
        response = {'calorie_intake': calorie_intake}
        return jsonify(response)

if __name__ == '__main__':
    app.run(port=9000, debug=True)