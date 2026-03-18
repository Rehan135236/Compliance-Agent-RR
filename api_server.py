import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Import our existing modules
from risk_engine import RiskEngine
from llm_explainer import LLMExplainer
from blockchain_risk import BlockchainRiskChecker

app = FastAPI(
    title="CIAA Enterprise Integration API",
    description="Compliance Intelligence AI Agent API for CRM and workflow integration.",
    version="1.0.0"
)

# Initialize engines
risk_engine = RiskEngine()
explainer = LLMExplainer()
blockchain_checker = BlockchainRiskChecker()

# In-memory "database" to track user history for the risk engine
# In production, this would grab from SQL/NoSQL
tx_history_db = []

class TransactionInput(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    country: str
    timestamp: str

class BlockchainInput(BaseModel):
    wallet_address: str

@app.get("/")
def read_root():
    return {"status": "ok", "service": "CIAA Enterprise API is running"}

@app.post("/api/v1/analyze_transaction")
def analyze_transaction(tx: TransactionInput):
    """
    Endpoint for external systems (CRMs, Marketing automation) 
    to send a transaction for live risk scoring.
    """
    try:
        tx_dict = tx.dict()
        
        # Build history dataframe
        history_df = pd.DataFrame(tx_history_db)
        
        # Score it
        analysis = risk_engine.score_transaction(tx_dict, history_df)
        
        # Add to history
        tx_history_db.append(tx_dict)
        
        # Explain it
        explanation = explainer.generate_explanation(
            tx_dict, 
            analysis['risk_score'], 
            analysis['risk_factors']
        )
        
        return {
            "transaction_id": tx.transaction_id,
            "status": "success",
            "risk_assessment": analysis,
            "ai_narrative": explanation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/assess_wallet")
def assess_wallet(wallet: BlockchainInput):
    """
    Endpoint for checking cryptocurrency wallet risk heuristically.
    """
    try:
        result = blockchain_checker.check_wallet(wallet.wallet_address)
        return {
            "wallet_address": wallet.wallet_address,
            "status": "success",
            "risk_assessment": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
