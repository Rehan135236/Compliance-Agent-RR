import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_transactions(num_rows=300):
    """
    Generates a sample dataset of financial transactions with a mix of 
    normal and suspicious patterns for the Compliance AI Agent.
    """
    np.random.seed(42)
    random.seed(42)

    user_ids = [f"USR{str(i).zfill(4)}" for i in range(1, 51)] # 50 unique users
    countries = ["USA", "GBR", "CAN", "DEU", "FRA", "RUS", "PRK", "IRN", "SYR", "CUB"]
    
    # High risk countries for AML
    high_risk_countries = ["RUS", "PRK", "IRN", "SYR", "CUB"]
    
    data = []
    
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_rows):
        tx_id = f"TXN{str(i+1).zfill(5)}"
        user_id = random.choice(user_ids)
        
        # Determine if this transaction should explicitly be an anomaly
        is_anomaly = random.random() < 0.15 # 15% chance of being suspicious
        
        if is_anomaly:
            # Anomalous patterns: high amount, high risk country
            amount = round(random.uniform(10000, 500000), 2)
            country = random.choices(countries, weights=[1]*5 + [5]*5, k=1)[0]
        else:
            # Normal patterns: smaller amounts, safe countries
            amount = round(random.uniform(10, 3000), 2)
            country = random.choices(countries, weights=[10]*5 + [1]*5, k=1)[0]
            
        # Add repeated rapid transactions pattern
        if i > 0 and random.random() < 0.05:
            # 5% chance to duplicate the user and date close together (structuring/smurfing)
            user_id = data[-1]['user_id']
            last_timestamp = datetime.strptime(data[-1]['timestamp'], "%Y-%m-%d %H:%M:%S")
            timestamp = last_timestamp + timedelta(minutes=random.randint(1, 15))
            amount = round(random.uniform(9000, 9999), 2) # Just below $10k reporting threshold
        else:
            timestamp = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
        data.append({
            'transaction_id': tx_id,
            'user_id': user_id,
            'amount': amount,
            'country': country,
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    df = pd.DataFrame(data)
    
    # Sort by timestamp to simulate real-world log
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    output_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} transactions and saved to {output_path}")

if __name__ == "__main__":
    generate_transactions()
