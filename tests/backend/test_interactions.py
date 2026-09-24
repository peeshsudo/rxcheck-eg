"""import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_search_drugs():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/v1/drugs/search?q=clop")
        assert r.status_code == 200
        """

"""
Pytest unit tests for interaction calculation engine.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import SeverityLevel

client = TestClient(app)


def test_interaction_check_success_no_conflicts():
    payload = {"drug_ids": ["drug_001"], "selected_foods": []}
    response = client.post("/api/v1/interactions/check", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["has_interactions"] is False
    assert len(data["schedules"]) == 1


def test_interaction_check_with_severe_conflict():
    payload = {"drug_ids": ["drug_002", "drug_003"], "selected_foods": []}
    response = client.post("/api/v1/interactions/check", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["has_interactions"] is True
    assert len(data["drug_interactions"]) >= 1
    assert data["drug_interactions"][0]["severity"] == SeverityLevel.SEVERE
    assert data["drug_interactions"][0]["requires_gp_consultation"] is True


def test_interaction_check_invalid_drug_id():
    payload = {"drug_ids": ["non_existent_drug"], "selected_foods": []}
    response = client.post("/api/v1/interactions/check", json=payload)
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()