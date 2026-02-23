import os
import tempfile
import importlib

def test_health_endpoint():
    # app.py içindeki db path sabit olduğu için, test ortamında izolasyon zor olabilir.
    # Bu test sadece endpoint ayakta mı onu kontrol eder.
    app_module = importlib.import_module("app")
    app = app_module.app
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"