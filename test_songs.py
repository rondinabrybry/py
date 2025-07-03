import pytest
from fastapi.testclient import TestClient
from main import app, songs

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_songs():
    """Reset the songs list before each test"""
    songs.clear()
    yield
    songs.clear()

@pytest.fixture
def sample_song():
    return {
        "id": 1,
        "title": "Test Song",
        "length": 180,
        "date_released": "2024-01-01T00:00:00",
        "price": 9.99
    }

@pytest.fixture
def sample_songs():
    return [
        {
            "id": 1,
            "title": "First Song",
            "length": 180,
            "date_released": "2024-01-01T00:00:00",
            "price": 9.99
        },
        {
            "id": 2,
            "title": "Second Song",
            "length": 240,
            "date_released": "2024-02-01T00:00:00",
            "price": 12.99
        }
    ]

def test_welcome_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hey"}

def test_get_songs_empty():
    response = client.get("/songs")
    assert response.status_code == 200
    assert response.json() == []

def test_get_songs_with_data(sample_songs):
    for song in sample_songs:
        client.post("/songs", json=song)
    response = client.get("/songs")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "First Song"
    assert response.json()[1]["title"] == "Second Song"

def test_create_song_success(sample_song):
    response = client.post("/songs", json=sample_song)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Song"
    assert response.json()["id"] == 1

def test_create_song_adds_to_list(sample_song):
    client.post("/songs", json=sample_song)
    response = client.get("/songs")
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Song"

def test_create_multiple_songs(sample_songs):
    for song in sample_songs:
        response = client.post("/songs", json=song)
        assert response.status_code == 200
    response = client.get("/songs")
    assert len(response.json()) == 2

def test_create_song_missing_fields():
    incomplete_song = {
        "title": "Incomplete Song",
        "length": 180
    }
    response = client.post("/songs", json=incomplete_song)
    assert response.status_code == 422

def test_create_song_wrong_data_types():
    invalid_song = {
        "id": "not_an_integer",
        "title": "Test Song",
        "length": "not_an_integer",
        "date_released": "2024-01-01T00:00:00",
        "price": "not_a_float"
    }
    response = client.post("/songs", json=invalid_song)
    assert response.status_code == 422

def test_create_song_invalid_datetime():
    invalid_song = {
        "id": 1,
        "title": "Test Song",
        "length": 180,
        "date_released": "invalid-date-format",
        "price": 9.99
    }
    response = client.post("/songs", json=invalid_song)
    assert response.status_code == 422

def test_update_song_success(sample_song):
    client.post("/songs", json=sample_song)
    updated_song = sample_song.copy()
    updated_song["title"] = "Updated Song"
    updated_song["price"] = 19.99
    response = client.put("/songs/0", json=updated_song)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Song"
    assert response.json()["price"] == 19.99

def test_delete_song_success(sample_song):
    client.post("/songs", json=sample_song)
    response = client.delete("/songs/0")
    assert response.status_code == 200
    assert response.json() == {"message": "Song deleted"}