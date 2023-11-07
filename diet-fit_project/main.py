from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default_route():
    print("default route")
    response = {'hello': 'world'}
    return jsonify(response)

# Calculate BMI
@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    gender = data.get('gender')
    age = data.get('age')
    height = data.get('height')
    weight = data.get('weight')

    # took this formula from - https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
    bmi = weight / ((height / 100) ** 2)

    response = {'bmi': bmi}
    return jsonify(response)

# Calculate Average Calorie Intake
@app.route('/calculate_calories', methods=['POST'])
def calculate_calories():
    data = request.get_json()
    gender = data.get('gender')
    bmi = data.get('bmi')

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
    response = {'calorie_intake': calorie_intake}
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9000, debug=True)