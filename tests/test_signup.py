from src import app as app_module


def test_signup_success_normalizes_email_and_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    submitted_email = "  NewStudent@Mergington.edu  "
    expected_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": submitted_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {expected_email} for {activity_name}"}
    assert expected_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_when_activity_does_not_exist(client):
    # Arrange
    missing_activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_invalid_email(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": invalid_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email"


def test_signup_returns_409_for_duplicate_email_with_different_formatting(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "  Michael@Mergington.edu  "

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": duplicate_email})

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": "new@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
