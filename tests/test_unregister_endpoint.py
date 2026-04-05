"""Tests for DELETE /activities/{activity_name}/signup endpoint."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering a student from an activity."""
    
    def test_unregister_successful(self, client):
        """
        Arrange: Prepare registered student email and activity name
        Act: Send DELETE request to unregister endpoint
        Assert: Verify student is removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify the student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_participant_not_found(self, client):
        """
        Arrange: Use email not registered for activity
        Act: Send DELETE request to unregister endpoint
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "not_registered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
    
    def test_unregister_activity_not_found(self, client):
        """
        Arrange: Use non-existent activity name
        Act: Send DELETE request to unregister endpoint
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_multiple_participants(self, client):
        """
        Arrange: Activity with multiple participants
        Act: Unregister one participant
        Assert: Verify only that participant is removed
        """
        # Arrange
        activity_name = "Drama Club"
        email_to_remove = "lucy@mergington.edu"
        email_to_keep = "james@mergington.edu"
        
        # Verify initial state
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities[activity_name]["participants"]) == 2
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify only the specified participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert len(activities[activity_name]["participants"]) == 1
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]
