from urllib.parse import quote


def test_remove_participant_deletes_existing_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants/{encoded_email}"
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities_response.json()[activity_name]["participants"]


def test_remove_participant_rejects_missing_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants/{encoded_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_remove_participant_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "new.student@mergington.edu"
    encoded_activity_name = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants/{encoded_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}