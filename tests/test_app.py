"""
Pruebas de integración API y verificación del comportamiento de Feature Toggles.
"""
import pytest
from app import app
from configcat_service import feature_toggle_service

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "calculadora-tbd-api"

def test_api_sumar(client):
    response = client.post("/api/sumar", json={"a": 15, "b": 25})
    assert response.status_code == 200
    assert response.get_json()["resultado"] == 40

def test_api_restar(client):
    response = client.post("/api/restar", json={"a": 30, "b": 12})
    assert response.status_code == 200
    assert response.get_json()["resultado"] == 18

def test_api_multiplicar_toggle_on(client):
    feature_toggle_service.set_override("multiplicacion_enabled", True)
    response = client.post("/api/multiplicar", json={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.get_json()["resultado"] == 20

def test_api_multiplicar_toggle_off(client):
    feature_toggle_service.set_override("multiplicacion_enabled", False)
    response = client.post("/api/multiplicar", json={"a": 4, "b": 5})
    assert response.status_code == 403
    assert response.get_json()["error"] == "FeatureDisabled"

def test_api_dividir_toggle_off(client):
    feature_toggle_service.set_override("division_enabled", False)
    response = client.post("/api/dividir", json={"a": 10, "b": 2})
    assert response.status_code == 403
    assert response.get_json()["error"] == "FeatureDisabled"

def test_api_dividir_toggle_on_y_error_cero(client):
    feature_toggle_service.set_override("division_enabled", True)
    # Test caso normal
    response = client.post("/api/dividir", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.get_json()["resultado"] == 5.0
    
    # Test caso división por cero
    response_cero = client.post("/api/dividir", json={"a": 10, "b": 0})
    assert response_cero.status_code == 400
    assert response_cero.get_json()["error"] == "ValidationError"
