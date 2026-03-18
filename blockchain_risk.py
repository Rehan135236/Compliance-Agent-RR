import random
import hashlib

class BlockchainRiskChecker:
    """
    Bonus Module: Simple Blockchain Transaction Risk Check.
    Simulates a risk check on a crypto wallet or transaction hash.
    """
    def __init__(self):
        # Simulated database of known bad actors/wallets
        self.known_bad_wallets = [
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", # Satoshi's wallet (just an example of well known)
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e", # Random hex
            "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
        ]
        
    def check_wallet(self, wallet_address):
        """
        Checks a wallet address for risk.
        Returns risk score 0-100 and reason.
        """
        if not wallet_address:
            return {"score": 0, "reason": "No wallet provided."}
            
        wallet_address = str(wallet_address).strip()
        
        # 1. Check known bad list
        if wallet_address in self.known_bad_wallets:
            return {"score": 95, "reason": "Wallet address is on known bad actors list (e.g. OFAC Sanctions)."}
            
        # 2. Simulate risk based on address hashing (for demo purposes)
        # This gives us deterministic but random-looking risk scores for any input
        hash_val = int(hashlib.sha256(wallet_address.encode('utf-8')).hexdigest(), 16)
        simulated_risk = (hash_val % 100)
        
        reason = "Wallet analyzed on blockchain. "
        if simulated_risk >= 75:
            reason += "Interaction with mixers or darknet markets detected."
        elif simulated_risk >= 40:
            reason += "Slightly elevated risk. Interaction with high-risk exchanges."
        else:
            reason += "Clean transaction history. Mined from reputable pool or standard exchange."
            
        return {"score": simulated_risk, "reason": reason}

if __name__ == "__main__":
    # Test Blockchain Risk Checker
    checker = BlockchainRiskChecker()
    print("Testing Known Bad:", checker.check_wallet("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"))
    print("Testing Random:", checker.check_wallet("0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"))
