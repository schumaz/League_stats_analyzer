# League of Legends Stats Analyzer 🎮

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458.svg)

An interactive, locally-hosted dashboard designed to analyze your League of Legends match history. Built with Python and Streamlit, this tool extracts data directly from the Riot Games API, processes your performance metrics, and visualizes them through dynamic charts.

## ✨ Features

* **Global & Role-Specific Overviews:** Filter your recent matches by position (Top, Jungle, Mid, ADC, Support) to see where you perform best.
* **Advanced Metrics:** Track Damage Per Minute (DPM), Gold Per Minute, Farm Per Minute, and Vision Scores over time.
* **Custom Chart Builder (X / Y):** Build your own scatter plots to find correlations (e.g., Match Duration vs. Total Damage) and color-code them by Champion.
* **In-Depth Champion Stats:** A dedicated tab to view your average KDA, objective damage, control wards bought, and play rates for specific champions.
* **Local Caching & Safe Reset:** Match history is saved locally in a `.json` database to avoid rate limits, with a secure double-confirmation reset button.

---

## 🚀 How to Run (Portable Version)

You **do not** need to install Python or any coding tools to run this app! It comes fully packaged with a portable environment.

1. Go to the [Releases] page of this repository.
2. Download the latest `LeagueStatsAnalyzer_Release.7z` file.
3. Extract the `.7z` folder anywhere on your computer.
4. Open the extracted folder and double-click **`start.bat`**.
5. A terminal window will appear, and your default web browser will automatically open the dashboard.
6. To close the app, you'll need to close the terminal window.

---

## 🔑 Setting up your Riot API Key

To download your matches, the app needs to securely communicate with the Riot Games servers. You will need a personal API Key.

1. Go to the [Riot Developer Portal](https://developer.riotgames.com/).
2. Log in with your League of Legends account.
3. Scroll down and click **"Regenerate API Key"** (or Generate).
4. Copy the long key.
5. Open the Stats Analyzer app in your browser, paste the key in the **Authentication** sidebar along with your Riot ID and Tag, and click **Save & Authenticate**.
6. Click **"Sync Recent Matches"** and enjoy your data!

> **Note:** Personal Development API keys expire every 24 hours. If the app stops syncing new matches, simply generate a new key on the Riot Portal and update it in the app's sidebar.

---

## 🛠️ Tech Stack

* **Backend:** Python, `riotwatcher` (Riot API wrapper).
* **Frontend:** Streamlit.
* **Data Processing:** Pandas.
* **Data Visualization:** Altair.

---
*Disclaimer: League of Legends Stats Analyzer isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.*
