"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""
    
    def test_signup_successful(self, client):
        """
        Arrange: Prepare student email and activity name
        Act: Send POST request to signup endpoint
        Assert: Verify student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify the student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_duplicate_email_returns_error(self, client):
        """
        Arrange: Use email already registered for activity
        Act: Send POST request to signup endpoint
        Assert: Verify duplicate signup is rejected
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_activity_not_found(self, client):
        """
        Arrange: Use non-existent activity name
        Act: Send POST request to signup endpoint
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_with_special_characters_in_email(self, client):
        """
        Arrange: Use email with special characters
        Act: Send POST request to signup endpoint
        Assert: Verify signup works with special characters
        """
        # Arrange
        activity_name = "Art Studio"
        email = "student+test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify the student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
