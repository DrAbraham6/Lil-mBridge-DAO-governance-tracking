# tests/test_agent3.py
import pytest
from fastapi.testclient import TestClient
from agent3_kernel import app, ledger

client = TestClient(app)

def test_ping():
    """Check that the ping endpoint returns online status."""
    response = client.get("/agent3/ping")
    assert response.status_code == 200
    assert response.json()["status"] == "Agent 3 online"

def test_txn_bank_as_fiat():
    """POST a bank transaction, verify it's treated as fiat and queued correctly."""
    # Clear ledger before test
    ledger.clear()

    txn_data = {
        "tx_id": "001",
        "source": "dao_vault",
        "destination": "wyoming_llc_bank",
        "amount": 100,
        "currency": "USD",
        "bridge": "bank"
    }

    response = client.post("/txn", json=txn_data)
    assert response.status_code == 200
    json_resp = response.json()

    # Bridge should have been converted to fiat
    assert json_resp["status"] == "queued_fiat"

    # Ledger should contain the transaction
    assert len(ledger) == 1
    assert ledger[0]["bridge"] == "fiat"
    assert ledger[0]["amount"] == 100
