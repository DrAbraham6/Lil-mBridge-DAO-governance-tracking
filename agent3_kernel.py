# agent3_kernel.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- Models ---
class Transaction(BaseModel):
    tx_id: str
    source: str
    destination: str
    amount: float
    currency: str  # "USD", "EUR", "USDC", "DAI"
    bridge: str    # "fiat", "crypto", "bank", "hybrid"

# --- Memory Store ---
ledger = []

# --- Core Routes ---
@app.post("/txn")
async def create_txn(txn: Transaction):
    # Convert "bank" bridge to "fiat"
    if txn.bridge == "bank":
        txn.bridge = "fiat"

    # Pydantic V2 compliant
    ledger.append(txn.model_dump())

    # Response based on bridge
    if txn.bridge == "fiat":
        return {"status": "queued_fiat", "txn": txn}
    elif txn.bridge == "crypto":
        return {"status": "queued_crypto", "txn": txn}
    else:
        return {"status": "hybrid", "txn": txn}

@app.get("/ledger")
async def get_ledger():
    return {"ledger": ledger}

# --- Agent Hooks ---
@app.get("/agent3/ping")
async def ping():
    return {"status": "Agent 3 online", "ledger_size": len(ledger)}
