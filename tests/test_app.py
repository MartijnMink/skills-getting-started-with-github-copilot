import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities

BASE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Soccer Team": {
        "description": "Weekly soccer practice and inter-school matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu"],
    },
    "Basketball Club": {
        "description": "Learn basketball skills, drills, and teamwork",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["mia@mergington.edu"],
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed-media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["noah@mergington.edu"],
    },
    "Drama Workshop": {
        "description": "Acting, stagecraft, and performance rehearsal",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu"],
    },
    "Science Olympiad": {
        "description": "Team science challenges, experiments, and tournaments",
        "schedule": "Tuesdays, 4:30 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu"],
    },
    "Math Club": {
        "description": "Problem solving, puzzles, and competition prep",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu"],
    },
}


@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(copy.deepcopy(BASE_ACTIVITIES))
    yield
    app_activities.clear()
    app_activities.update(copy.deepcopy(BASE_ACTIVITIES))


client = TestClient(app)


def test_get_activities_returns_current_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"


def test_post_signup_succeeds():
    # Arrange
    signup_email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": signup_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {signup_email} for Chess Club"}
    assert signup_email in app_activities["Chess Club"]["participants"]


def test_post_signup_duplicate_returns_400():
    # Arrange
    signup_email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": signup_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_post_signup_unknown_activity_returns_404():
    # Arrange
    signup_email = "someone@mergington.edu"

    # Act
    response = client.post("/activities/Nonexistent/signup", params={"email": signup_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_participant_succeeds():
    # Arrange
    remove_email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": remove_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {remove_email} from Chess Club"}
    assert remove_email not in app_activities["Chess Club"]["participants"]


def test_delete_missing_participant_returns_404():
    # Arrange
    remove_email = "notregistered@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants", params={"email": remove_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"