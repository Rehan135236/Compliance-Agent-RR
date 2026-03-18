import os
import openai

class LLMExplainer:
    """
    Uses OpenAI API to explain why a transaction is flagged and summarize patterns.
    If no API key is provided, falls back to a rule-based mock explanation generator
    to ensure the application remains functional.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
            
    def generate_explanation(self, transaction_data, risk_score, risk_factors):
        """
        Generates a natural language explanation for a flagged transaction.
        """
        if not risk_factors:
            return "This transaction appears normal based on current risk parameters."
            
        factors_text = "\n- ".join(risk_factors)
        
        # Fallback if no OpenAI Key
        if not self.client:
            return self._mock_explanation(transaction_data, risk_score, risk_factors)
            
        prompt = f"""
        You are an expert Anti-Money Laundering (AML) and Compliance Analyst AI.
        
        Analyze the following flagged transaction and provide a concise, professional explanation 
        (max 3 sentences) of why it is considered risky.
        
        Transaction Details:
        - ID: {transaction_data.get('transaction_id')}
        - Amount: ${transaction_data.get('amount'):,.2f}
        - Country: {transaction_data.get('country')}
        - Timestamp: {transaction_data.get('timestamp')}
        
        Risk Score: {risk_score}/100
        
        Risk Factors Identified by Engine:
        - {factors_text}
        
        Provide your summary:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a specialized compliance AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM API Error: {str(e)}")
            return self._mock_explanation(transaction_data, risk_score, risk_factors)
            
    def _mock_explanation(self, transaction_data, risk_score, risk_factors):
        """
        Generates a deterministic text explanation if API is unavailable.
        """
        risk_level = "High" if risk_score > 70 else ("Medium" if risk_score > 30 else "Low")
        
        explanation = f"This transaction from {transaction_data.get('country')} for ${transaction_data.get('amount'):,.2f} "
        explanation += f"is flagged as {risk_level} Risk (Score: {risk_score}). "
        
        if "velocity" in str(risk_factors).lower() or "rapid" in str(risk_factors).lower():
            explanation += "It displays patterns consistent with rapid, repeated transfers within a short timeframe. "
        if "structuring" in str(risk_factors).lower():
            explanation += "The amount is just below standard reporting thresholds, which may indicate structuring or 'smurfing'. "
        if "high-risk" in str(risk_factors).lower() or "country" in str(risk_factors).lower():
            explanation += "Additionally, it involves a jurisdiction known for elevated AML risk."
            
        return explanation.strip()

if __name__ == "__main__":
    # Test Mock Explainer
    explainer = LLMExplainer()
    tx = {
        'transaction_id': 'TXN123',
        'amount': 45000,
        'country': 'RUS',
        'timestamp': '2023-10-27 10:00:00'
    }
    factors = [
        "High transaction amount ($45,000.00) exceeds $10,000.00 threshold.",
        "Destination/Origin country (RUS) is on the high-risk watch list.",
        "Rapid succession: Another transaction detected within 60 minutes."
    ]
    print(explainer.generate_explanation(tx, 95, factors))
