from flask import Flask, render_template
from predict import predict_team_success
from scrape import scrape_points_and_schedule

app = Flask(__name__)

# Load scraped data at startup
points_data, schedule_data = scrape_points_and_schedule()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/points-table')
def points_table():
    return render_template("points_table.html", points=points_data)

@app.route('/schedule')
def schedule():
    return render_template("schedule.html", schedule=schedule_data)

@app.route('/predict/<team_name>')
def predict(team_name):
    result = predict_team_success(team_name)
    return render_template("points_table.html", points=points_data, result=result)

if __name__ == '__main__':
    app.run(debug=True)
