import os
from datetime import datetime
from fpdf import FPDF
import pandas as pd

class ReportGenerator:
    """
    Generates Suspicious Activity Reports (SAR) and Risk Summaries
    in Text or PDF formats.
    """
    def __init__(self, output_dir=None):
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), 'reports')
        
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_text_sar(self, transaction, explanation):
        """Generates a text-based SAR."""
        report_id = f"SAR-{transaction['transaction_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        filename = os.path.join(self.output_dir, f"{report_id}.txt")
        
        content = f"""
=========================================================
          SUSPICIOUS ACTIVITY REPORT (SAR)
=========================================================
Report ID: {report_id}
Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--- SUBJECT INFORMATION ---
User ID: {transaction['user_id']}

--- TRANSACTION DETAILS ---
Transaction ID: {transaction['transaction_id']}
Timestamp: {transaction['timestamp']}
Amount: ${transaction['amount']:,.2f}
Country: {transaction['country']}

--- RISK ASSESSMENT ---
Risk Score: {transaction['risk_score']}/100
Risk Label: {transaction['risk_label']}
Risk Factors: 
{transaction['risk_factors']}

--- AI EXPLANATION / NARRATIVE ---
{explanation}

=========================================================
CONFIDENTIAL - FOR INTERNAL COMPLIANCE USE ONLY
=========================================================
"""
        with open(filename, 'w') as f:
            f.write(content.strip())
            
        return filename
        
    def generate_pdf_sar(self, transaction, explanation):
        """Generates a PDF SAR."""
        report_id = f"SAR-{transaction['transaction_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        filename = os.path.join(self.output_dir, f"{report_id}.pdf")
        
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "SUSPICIOUS ACTIVITY REPORT (SAR)", ln=True, align='C')
        pdf.ln(5)
        
        # Meta info
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 5, f"Report ID: {report_id}", ln=True)
        pdf.cell(0, 5, f"Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.line(10, 35, 200, 35)
        pdf.ln(10)
        
        # Subject & Tx Data
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Subject & Transaction Details", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 7, f"User ID: {transaction['user_id']}", ln=True)
        pdf.cell(0, 7, f"Transaction ID: {transaction['transaction_id']}", ln=True)
        pdf.cell(0, 7, f"Timestamp: {transaction['timestamp']}", ln=True)
        pdf.cell(0, 7, f"Amount: ${transaction['amount']:,.2f}", ln=True)
        pdf.cell(0, 7, f"Country: {transaction['country']}", ln=True)
        pdf.ln(5)
        
        # Risk assessment
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Risk Assessment", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(0, 7, f"Risk Score: {transaction['risk_score']}/100 ({transaction['risk_label']})", ln=True)
        pdf.multi_cell(0, 7, f"Risk Factors: {transaction['risk_factors']}")
        pdf.ln(5)
        
        # Narrative
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "AI Explanation / Narrative", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, explanation)
        pdf.ln(15)
        
        # Footer
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "CONFIDENTIAL - FOR INTERNAL COMPLIANCE USE ONLY", ln=True, align='C')
        
        pdf.output(filename)
        return filename

if __name__ == "__main__":
    # Test Report Generator
    rg = ReportGenerator()
    tx = {
        'transaction_id': 'TXN123',
        'user_id': 'USR01',
        'amount': 45000,
        'country': 'RUS',
        'timestamp': '2023-10-27 10:00:00',
        'risk_score': 95,
        'risk_label': 'High Risk',
        'risk_factors': 'High amount; High risk country'
    }
    explanation = "This transaction was flagged due to the high transfer amount to a high-risk jurisdiction, indicating potential money laundering activity."
    
    txt_path = rg.generate_text_sar(tx, explanation)
    pdf_path = rg.generate_pdf_sar(tx, explanation)
    
    print(f"Generated text SAR: {txt_path}")
    print(f"Generated PDF SAR: {pdf_path}")
