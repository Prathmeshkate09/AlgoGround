import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "total_questions" in data

def test_list_questions_unfiltered():
    response = client.get("/api/v1/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4
    assert any(q["slug"] == "pair-target-finder" for q in data)

def test_list_questions_filter_category():
    response = client.get("/api/v1/questions?category=SQL")
    assert response.status_code == 200
    data = response.json()
    assert all(q["category"] == "SQL" for q in data)

def test_list_questions_filter_difficulty():
    response = client.get("/api/v1/questions?difficulty=Easy")
    assert response.status_code == 200
    data = response.json()
    assert all(q["difficulty"] == "Easy" for q in data)

def test_list_questions_search():
    response = client.get("/api/v1/questions?search=Symmetry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "symmetry" in data[0]["title"].lower()

def test_get_single_question():
    response = client.get("/api/v1/questions/q-101")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "q-101"
    assert data["slug"] == "pair-target-finder"

def test_submit_valid_solution():
    payload = {
        "question_id": "q-101",
        "user_id": "test_user_42",
        "language": "javascript",
        "code": "function findPair(nums, target) { return [0, 1]; }"
    }
    response = client.post("/api/v1/submissions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["question_id"] == "q-101"
    assert data["status"] == "Accepted"
    assert data["passed_tests"] > 0

def test_user_progress_tracking():
    response = client.get("/api/v1/progress/test_user_42")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_42"
    assert "q-101" in data["solved_question_ids"]
