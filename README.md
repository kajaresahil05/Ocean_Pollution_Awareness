# Ocean Pollution Awareness

A Flask-based educational web application that raises awareness about ocean pollution through interactive content, visual data, quizzes, stories, and contact forms.

## Overview

This project presents information about major ocean pollution issues, marine ecosystems, historical pollution disasters, and practical ways people can help protect the oceans. It combines educational content with interactive charts and a simple user account flow.

## Features

- User registration and login
- Dashboard home page with ocean awareness content
- Ocean facts page with:
  - bar chart of total pollution by ocean
  - pie chart showing plastic, chemical, and metal pollution breakdown
  - interactive world map linking to ocean-specific pages
- Ocean-specific detail pages for:
  - Pacific Ocean
  - Atlantic Ocean
  - Indian Ocean
  - Southern Ocean
  - Arctic Ocean
- Ocean news and action page with solutions and calls to action
- Quiz on ocean pollution knowledge
- Quiz result leaderboard
- Story submission form
- Feedback and contact forms
- SQLite-based data storage for users, stories, feedback, quiz results, and contact messages

## Project Structure

- app.py - Main Flask application with routes, database models, and chart generation
- ocean_pollution_data.csv - Pollution dataset used for charts and analysis
- static/ - Images and videos used in the app
- instance/ - SQLite database files generated at runtime

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Pandas
- Plotly
- SQLite

## Installation

1. Navigate to the project folder:
   ```bash
   cd /home/apsit/Sahil/Ocean_Pollution_Awareness
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install flask flask_sqlalchemy pandas plotly
   ```

## Running the Application

Start the app with:

```bash
python3 app.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000
```

The first run will automatically create the SQLite database files in the instance folder.

## Main Routes

- /register - Create an account
- /login - Sign in
- /dashboard - Main landing page
- /ocean_facts - Interactive pollution charts and map
- /ocean_news - News, solutions, quiz link, and action section
- /quiz - Ocean pollution quiz
- /quiz_results - Quiz leaderboard
- /contact_us - Contact and feedback form
- /about_us - Project mission and information

## Notes

- The app uses inline HTML templates inside the Flask routes for the UI.
- Static media files such as images and videos are stored in the static folder.
- The app is intended for educational and awareness purposes.
