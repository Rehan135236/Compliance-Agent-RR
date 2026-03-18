import pandas as pd
import numpy as np
from datetime import datetime

class RiskEngine:
    """
    Analyzes financial transactions and assigns risk scores (0-100).
    """
    def __init__(self):
        # Configuration parameters
        self.amount_threshold_low = 5000
        self.amount_threshold_high = 10000
        self.rapid_tx_window_minutes = 60
        
        self.high_risk_countries = ["RUS", "PRK", "IRN", "SYR", "CUB"]
        self.medium_risk_countries = ["PAN", "BHS", "CYM"]
        
    def score_transaction(self, tx, user_history):
        """
        Scores a single transaction.
        tx: Series or Dict with transaction data
        user_history: DataFrame of previous transactions for this user
        """
        score = 0
        risk_factors = []
        
        amount = float(tx['amount'])
        country = tx['country']
        timestamp = pd.to_datetime(tx['timestamp'])
        
        # 1. Amount Risk (0-40 points)
        if amount > self.amount_threshold_high:
            score += 40
            risk_factors.append(f"High transaction amount (${amount:,.2f}) exceeds ${self.amount_threshold_high:,.2f} threshold.")
        elif amount > self.amount_threshold_low:
            score += 20
            risk_factors.append(f"Elevated transaction amount (${amount:,.2f}).")
            
        # 2. Country Risk (0-30 points)
        if country in self.high_risk_countries:
            score += 30
            risk_factors.append(f"Destination/Origin country ({country}) is on the high-risk watch list.")
        elif country in self.medium_risk_countries:
            score += 15
            risk_factors.append(f"Destination/Origin country ({country}) is considered medium risk.")
            
        # 3. Frequency/Structuring Risk (0-30 points)
        if not user_history.empty:
            # Check for multiple transactions in the recent window
            recent_txs = user_history[
                (user_history['timestamp'] >= timestamp - pd.Timedelta(minutes=self.rapid_tx_window_minutes)) &
                (user_history['transaction_id'] != tx['transaction_id'])
            ]
            
            if len(recent_txs) >= 2:
                score += 30
                risk_factors.append(f"High velocity: {len(recent_txs)} other transactions detected within {self.rapid_tx_window_minutes} minutes.")
            elif len(recent_txs) == 1:
                score += 15
                risk_factors.append(f"Rapid succession: Another transaction detected within {self.rapid_tx_window_minutes} minutes.")
                
            # Check for structuring (amounts just under 10k threshold)
            if 9000 <= amount < 10000 and len(recent_txs) > 0:
                score += 20
                risk_factors.append(f"Potential structuring: Amount (${amount:,.2f}) is just below reporting threshold with recent activity.")
                
        # Cap score at 100
        final_score = min(score, 100)
        
        # Determine Label
        if final_score <= 30:
            label = "Low Risk"
        elif final_score <= 70:
            label = "Medium Risk"
        else:
            label = "High Risk"
            
        return {
            'risk_score': final_score,
            'risk_label': label,
            'risk_factors': risk_factors
        }
        
    def analyze_dataset(self, df):
        """
        Analyzes an entire DataFrame of transactions and appends risk scores.
        """
        # Ensure timestamp is datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        results = []
        
        # We need to process chronologically to build history correctly
        df = df.sort_values(by='timestamp')
        
        for idx, row in df.iterrows():
            user_id = row['user_id']
            # Get user history up to this transaction
            user_history = df[(df['user_id'] == user_id) & (df['timestamp'] <= row['timestamp'])]
            
            analysis = self.score_transaction(row, user_history)
            
            # Combine original row with analysis
            row_dict = row.to_dict()
            row_dict.update({
                'risk_score': analysis['risk_score'],
                'risk_label': analysis['risk_label'],
                'risk_factors': "; ".join(analysis['risk_factors'])
            })
            results.append(row_dict)
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    # Simple test
    print("Testing Risk Engine...")
    engine = RiskEngine()
    
    test_tx = {
        'transaction_id': 'TXN123',
        'user_id': 'USR01',
        'amount': 15000,
        'country': 'SYR',
        'timestamp': datetime.now()
    }
    
    empty_history = pd.DataFrame()
    res = engine.score_transaction(test_tx, empty_history)
    print(f"Test Score: {res['risk_score']} - {res['risk_label']}")
    print(f"Factors: {res['risk_factors']}")
