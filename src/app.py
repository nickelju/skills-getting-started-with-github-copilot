"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team basketball practice and friendly matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Soccer drills, teamwork, and weekend scrimmages",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Drawing, painting, and mixed media projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["mia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and school theater productions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["evelyn@mergington.edu", "abigail@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Advanced problem-solving and math competition prep",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Society": {
        "description": "Critical thinking, public speaking, and formal debates",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["elijah@mergington.edu", "lucas@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate email
    normalized_email = email.strip().lower()
    if not normalized_email or "@" not in normalized_email:
        raise HTTPException(status_code=400, detail="Invalid email")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signup
    participants = activity["participants"]
    normalized_participants = {participant.strip().lower()
                               for participant in participants}
    if normalized_email in normalized_participants:
        raise HTTPException(status_code=409,
                            detail="Student already signed up for this activity")

    # Enforce capacity limit
    if len(participants) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    participants.append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
