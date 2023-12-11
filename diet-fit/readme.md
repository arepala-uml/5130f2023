# Diet Fit App

This Flask-powered web application is designed to help users calculate their BMI and estimate their average calorie intake, using their personal information as input. In the future, the application will also provide tailored diet plans for users in the weeks ahead

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Prerequisites

To run this application, you need to have the following software installed on your system:

- python3
- pip3 (Python package manager)

## Installation (Creating python virtual environment)
1. change the directory to `~/5130f2023/diet-fit_project`
```
cd ~/5130f2023/diet-fit_project
```
2. create a virtual env( this is done only once)
```
python3 -m venv venv
```
3. activate the virtual env
```
source venv/bin/activate
```
4. install the dependencies
```
pip3 install -r requirements.txt
```

5. Install docker based on your OS

6. Bring up the mongoDB container using the docker-compose file
```
cd ~/5130f2023/diet-fit_project; docker-compose up -d
```

## Usage 
1. change the directory to `~/5130f2023/diet-fit_project`
```
cd ~/5130f2023/diet-fit_project
```
2. activate the virtual env
```
source venv/bin/activate
```
3. start the flask server
```
python3 main.py
```

3. To access the application, open the below url in the browser 
```
http://localhost:9000/
```