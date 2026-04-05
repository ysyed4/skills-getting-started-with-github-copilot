"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Use the test client
        Act: Send GET request to /activities
        Assert: Verify all activities are returned
        """
        # Arrange (implicit: client fixture provides TestClient)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_returns_correct_structure(self, client):
        """
        Arrange: Use the test client
        Act: Send GET request to /activities
        Assert: Verify activity structure is correct
        """
        # Arrange (implicit: client fixture provides TestClient)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_includes_participants(self, client):
        """
        Arrange: Use the test client
        Act: Send GET request to /activities
        Assert: Verify participants are included
        """
        # Arrange (implicit: client fixture provides TestClient)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
