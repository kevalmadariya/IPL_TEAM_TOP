# IPL Team Top Predictor 🔝🏏

**Live App:** [ipl-team-top.onrender.com](https://ipl-team-top.onrender.com/)

This project predicts whether a selected IPL team can still **top the points table** by the end of the tournament. It uses real-time IPL data via **web scraping** and models the problem using a **bipartite graph** with a **Max-Flow algorithm** to determine feasibility.

---

## 🚀 Features

- ✅ Select any IPL team and check if it can still finish at the top of the league table.
- 🌐 Real-time data scraping from official sources for live IPL stats.
- 🔗 Intuitive UI deployed on Render.
- 📈 Graph-based algorithm using **Max-Flow on a Bipartite Graph**:
  - One part of the graph: **Remaining matches**
  - Other part: **Teams**
  - Includes a **source** and **sink** node to calculate flow.
- ⚙️ If **max-flow == number of remaining matches**, then it's **mathematically possible** for the team to finish on top.

---

## 🛠 Tech Stack

- **Python** (Backend logic & scraping)
- **Flask / FastAPI** (Web server)
- **BeautifulSoup / Requests** (Web scraping)
- **NetworkX** (Graph construction and max-flow algorithm)
- **HTML/CSS/JS** (Frontend)
- **Render** (Deployment platform)

---

## 📊 How It Works

1. Scrape current IPL standings and schedule.
2. Build a bipartite graph:
   - Nodes: Teams & Matches
   - Edges: Match-to-team, respecting possible outcomes
3. Add a source and sink node.
4. Use Max-Flow to check if the selected team can still win enough matches to top the league.
5. Show result on the web UI: **"Yes, can top!"** or **"No, not possible."**

---
