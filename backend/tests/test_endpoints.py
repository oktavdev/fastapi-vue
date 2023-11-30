from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


class TestLiveWeather:
    # We are testing the live endpoint, and it makes call to external API. 
    # TODO: add tests with abstraction of external API by mocking the response

    def test_get_weather_with_valid_input(self):
        # Test with valid latitude and longitude
        response = client.get("/weather?latitude=40.7128&longitude=-74.0060")
        assert response.status_code == 200
        assert "weather" in response.json()

    def test_get_weather_with_invalid_input(self):
        response = client.get("/weather?latitude=invalid&longitude=-74.0060")
        assert response.status_code == 422
        assert "type_error" in response.json()["detail"][0]["type"]

