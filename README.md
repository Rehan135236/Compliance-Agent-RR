# 🕵️‍♂️ Compliance Intelligence AI Agent (CIAA)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Compliance Intelligence AI Agent (CIAA)** is a production-ready, enterprise-grade AI system designed for Anti-Money Laundering (AML) monitoring, risk analysis, and automated compliance reporting. It leverages rule-based anomaly detection alongside Large Language Models (LLMs) to provide transparent, explainable insights into suspicious financial activities.

---

## 🌟 Key Features

1. **Transaction Analysis Engine**
   - Ingests CSV transaction data and evaluates user history.
   - Algorithmically detects high-value anomalies, rapid structuring (smurfing), and geographic risk exposure.

2. **Automated Risk Scoring System**
   - Assesses transactions on a continuous 0-100 scale.
   - Deterministic ruleset assigns clear risk labels: **Low Risk** (0–30), **Medium Risk** (31–70), and **High Risk** (71–100).

3. **AI Explanation Module (LLM)**
   - Integrates with OpenAI's API to synthesize complex risk factors into natural language summaries.
   - Includes an intelligent deterministic fallback if an API key is unavailable.

4. **Compliance Report Generator**
   - Automatically generates formal **Suspicious Activity Reports (SAR)**.
   - Exports reports in both PDF and Text formats for seamless internal or regulatory consumption.

5. **Interactive Streamlit Dashboard**
   - Modern, responsive web interface for Compliance Analysts.
   - Features dynamic filtering, realtime metric aggregation, and direct AI chat interactions.

6. **🚀 Bonus: Blockchain Risk Check**
   - Built-in simulator module for assessing the risk of cryptocurrency wallet addresses and transaction hashes based on known threat actor databases and heuristic patterns.

---

## 🏗️ Architecture & Project Structure

```text
/compliance_ai_agent
│── app.py                 # Main Streamlit dashboard application
│── risk_engine.py         # Core logic for analyzing and scoring transaction risk
│── data_generator.py      # Utility to generate realistic mock transaction datasets
│── llm_explainer.py       # OpenAI integration and natural language generation
│── report_generator.py    # Formatting and exporting of PDF/TXT SAR documents
│── blockchain_risk.py     # Bonus: Crypto wallet risk simulator module
│── sample_data.csv        # Example generated dataset
│── requirements.txt       # Project dependencies
│── README.md              # Project documentation
│── /reports               # Directory for exported SARs (auto-generated)
```

---

## ⚡ Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/compliance_ai_agent.git
cd compliance_ai_agent
pip install -r requirements.txt
```

### 3. Generate Sample Data
Run the data generator to create a robust dataset (`sample_data.csv`) of ~300 transactions containing both normal and suspicious patterns:

```bash
python data_generator.py
```

### 4. (Optional) Configure AI Integration
To enable real LLM explanations, set your OpenAI API key in your environment:

```bash
# Windows
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```
*(If no key is provided, the application will automatically use a deterministic text fallback).*

### 5. Launch the Dashboard
Start the Streamlit interface:

```bash
streamlit run app.py
```
*Navigate to `http://localhost:8501` in your browser.*

---

## 📊 Example Workflows & Outputs

### 1. Triaging High Risk
From the dashboard, filter by **High Risk Only**. The Metrics panel will actively reflect the total number of flagged entities. Click on a specific transaction ID to review raw data and risk parameters.

### 2. Exporting an SAR
Within the "AI Explainer & Reporting" tab, click `Generate AI Explanation & Run Report`. The AI will produce a summary like:
> *"This transaction is flagged due to an unusually high amount ($45,000) sent to a high-risk jurisdiction (RUS). Furthermore, it displays patterns consistent with rapid transfer structuring."*

You can immediately single-click download the **PDF SAR** for the transaction.

### 3. Validating a Crypto Wallet
Navigate to the **Blockchain Risk Check** tab, enter an address (e.g., `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`), and instantly receive a simulated heuristic risk score.

---
*Developed for advanced compliance ecosystems.*
