from flask import Flask, render_template, jsonify
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from predict import predict_team_success


app = Flask(__name__)

# Function to run scraping script periodically
def update_data():
    os.system("python scrape.py")

# Schedule the scraping script to run every 3 hours
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', hours=3)
scheduler.start()

# Load data from JSON
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/points-table')
def points_table():
    points_data = load_data("points_table.json")
    return render_template("points_table.html", points=points_data)

@app.route('/schedule')
def schedule():
    schedule_data = load_data("schedule.json")
    return render_template("schedule.html", schedule=schedule_data)

@app.route('/predict/<team_name>')
def predict(team_name):
    result = predict_team_success(team_name)
    print(result)
    points_data = load_data("points_table.json")
    return render_template("points_table.html",points=points_data,result = result)

if __name__ == '__main__':
    app.run(debug=True)
