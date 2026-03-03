def test_get_activities_returns_activity_dictionary(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload

    first_activity_details = next(iter(payload.values()))
    assert required_fields.issubset(first_activity_details.keys())
