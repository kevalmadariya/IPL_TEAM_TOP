from flask import Flask, render_template
from predict import predict_team_success
from scrape import scrape_points_and_schedule
import os

app = Flask(__name__)

# Load scraped data at startup
points_data, schedule_data , orange_cap_data, purple_cap_data = scrape_points_and_schedule()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/points-table')
def points_table():
    return render_template("points_table.html", points=points_data)

@app.route('/schedule')
def schedule():
    return render_template("schedule.html", schedule=schedule_data)

@app.route('/predict/<id>')
def predict(id):
    result = predict_team_success(id,points_data,schedule_data)
    print(result)
    return render_template("points_table.html", points=points_data, result=result)


@app.route('/orange_cap')
def orange_cap():
    return render_template("orange_cap.html",orange_cap_data = orange_cap_data)

@app.route('/purple_cap')
def puple_cap():
    return render_template("purple_cap.html",purple_cap_data = purple_cap_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# from flask import Flask, render_template
# import json
# import os
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from predict import predict_team_success
# import datetime
# import requests
# import base64
# import os
# from datetime import datetime

# app = Flask(__name__)

# #f
# def push_to_github(file_path, repo, branch="main"):
#     token = os.getenv("GITHUB_TOKEN")
#     if not token:
#         print("No GitHub token found!")
#         return

#     headers = {
#         "Authorization": f"token {token}",
#         "Accept": "application/vnd.github+json"
#     }

#     # Read file content and encode in base64
#     with open(file_path, "rb") as f:
#         content = base64.b64encode(f.read()).decode("utf-8")

#     # Get the current file SHA
#     filename = os.path.basename(file_path)
#     url = f"https://api.github.com/repos/{repo}/contents/{filename}"

#     response = requests.get(url, headers=headers)
#     sha = response.json().get("sha")

#     data = {
#         "message": f"Update {filename} at {datetime.now()}",
#         "content": content,
#         "branch": branch,
#         "sha": sha  # Include for updates
#     }

#     response = requests.put(url, json=data, headers=headers)

#     if response.status_code == 200 or response.status_code == 201:
#         print(f"{filename} pushed successfully!")
#     else:
#         print("Failed to push file:", response.json())

# # Function to run scraping script periodically
# def update_data():
#     os.system("python scrape.py")
#     push_to_github("points_table.json", "kevalmadariya/IPL_TEAM_TOP")
#     push_to_github("schedule.json", "kevalmadariya/IPL_TEAM_TOP")

# # Schedule the scraping script to run every 3 hours
# scheduler = BackgroundScheduler()
# scheduler.add_job(update_data, 'interval', hours=1/60)
# scheduler.start()
# # Schedule to run at 11:30 PM
# # scheduler.add_job(update_data, CronTrigger(hour=23, minute=30))
# # # Schedule to run at 7:30 PM (19:30)
# # scheduler.add_job(update_data, CronTrigger(hour=19, minute=30))

# # scheduler.start()

# # Load data from JSON
# def load_data(filename):
#     with open(filename, "r") as f:
#         return json.load(f)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/points-table')
# def points_table():
#     points_data = load_data("points_table.json")
#     return render_template("points_table.html", points=points_data)

# @app.route('/schedule')
# def schedule():
#     schedule_data = load_data("schedule.json")
#     return render_template("schedule.html", schedule=schedule_data)

# @app.route('/predict/<team_name>')
# def predict(team_name):
#     result = predict_team_success(team_name)
#     print(result)
#     points_data = load_data("points_table.json")
#     return render_template("points_table.html",points=points_data,result = result)

# # local
# if __name__ == '__main__':
#     app.run(debug=True)

    # # if __name__ == "__main__":
    # #     app.run(host="0.0.0.0", port=5000)