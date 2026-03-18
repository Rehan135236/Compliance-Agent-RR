import streamlit as st
import pandas as pd
import os
import io

from risk_engine import RiskEngine
from llm_explainer import LLMExplainer
from report_generator import ReportGenerator
from blockchain_risk import BlockchainRiskChecker

# Set page config
st.set_page_config(
    page_title="Compliance Intelligence AI Agent", 
    page_icon="🕵️‍♂️", 
    layout="wide"
)

# Initialize engines
@st.cache_resource
def load_engines():
    return RiskEngine(), LLMExplainer(), ReportGenerator(), BlockchainRiskChecker()

risk_engine, llm_explainer, report_generator, blockchain_checker = load_engines()

# Simple RBAC (Role-Based Access Control)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

if not st.session_state['authenticated']:
    st.title("🔒 CIAA Enterprise Login")
    st.markdown("Please authenticate to access the Compliance Intelligence AI Agent.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Mock Enterprise Auth
            if username == "admin" and password == "admin":
                st.session_state['authenticated'] = True
                st.session_state['user_role'] = "Administrator"
                st.session_state['username'] = username
                st.rerun()
            elif username == "analyst" and password == "analyst":
                st.session_state['authenticated'] = True
                st.session_state['user_role'] = "Compliance Analyst"
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Invalid credentials. Try admin/admin or analyst/analyst")
    st.stop() # Stop rendering the rest of the app

# Header (Only shows if authenticated)
st.title("🕵️‍♂️ Compliance Intelligence AI Agent (CIAA)")
st.markdown("### Enterprise Anti-Money Laundering (AML) & Risk Analysis Dashboard")
st.caption(f"Logged in as: **{st.session_state['username']}** | Role: **{st.session_state['user_role']}**")
st.markdown("---")

# Sidebar
st.sidebar.header("Configuration & Upload")
uploaded_file = st.sidebar.file_uploader("Upload Transaction Data (CSV)", type="csv")

if 'data_analyzed' not in st.session_state:
    st.session_state['data_analyzed'] = False
if 'results_df' not in st.session_state:
    st.session_state['results_df'] = pd.DataFrame()

# Main logic
if uploaded_file is not None or st.sidebar.button("Load Sample Data"):
    with st.spinner("Loading and analyzing transactions..."):
        try:
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
            else:
                sample_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
                if os.path.exists(sample_path):
                    df = pd.read_csv(sample_path)
                else:
                    st.error("Sample data not found. Please run data_generator.py first.")
                    st.stop()
                    
            # Analyze Dataset
            results_df = risk_engine.analyze_dataset(df)
            st.session_state['results_df'] = results_df
            st.session_state['data_analyzed'] = True
            st.sidebar.success("Analysis Complete!")
        except Exception as e:
            st.error(f"Error processing data: {e}")

if st.session_state['data_analyzed']:
    results_df = st.session_state['results_df']
    
    # ---------------- Metrics ---------------- #
    total_tx = len(results_df)
    high_risk_count = len(results_df[results_df['risk_label'] == 'High Risk'])
    medium_risk_count = len(results_df[results_df['risk_label'] == 'Medium Risk'])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", total_tx)
    col2.metric("High Risk Flags", high_risk_count, delta_color="inverse")
    col3.metric("Medium Risk Flags", medium_risk_count, delta_color="inverse")
    col4.metric("Clean Transactions", total_tx - high_risk_count - medium_risk_count)
    
    st.markdown("---")
    
    # ---------------- Tabs ---------------- #
    tab1, tab2, tab3 = st.tabs(["📊 Transaction Analysis", "🤖 AI Explainer & Reporting", "🔗 Blockchain Risk Check"])
    
    with tab1:
        st.subheader("Flagged Transactions Overview")
        # Filter for display
        filter_level = st.selectbox("Filter Risk Level:", ["All Flagged (High & Medium)", "High Risk Only", "Medium Risk Only", "Low Risk Only", "All Transactions"])
        
        display_df = results_df.copy()
        if "High & Medium" in filter_level:
            display_df = display_df[display_df['risk_label'].isin(['High Risk', 'Medium Risk'])]
        elif "High Risk" in filter_level:
            display_df = display_df[display_df['risk_label'] == 'High Risk']
        elif "Medium Risk" in filter_level:
            display_df = display_df[display_df['risk_label'] == 'Medium Risk']
        elif "Low Risk" in filter_level:
            display_df = display_df[display_df['risk_label'] == 'Low Risk']
            
        # Display Dataframe with color formatting
        def color_risk(val):
            if val == 'High Risk': return 'color: red; font-weight: bold'
            elif val == 'Medium Risk': return 'color: orange; font-weight: bold'
            return 'color: green'
            
        st.dataframe(
            display_df.style.map(color_risk, subset=['risk_label']),
            use_container_width=True,
            height=400
        )
        
    with tab2:
        st.subheader("Deep Dive & SAR Generation")
        
        if len(display_df) == 0:
            st.info("No transactions selected in the active filter.")
        else:
            col_a, col_b = st.columns([1, 2])
            
            with col_a:
                selected_tx_id = st.selectbox("Select a Transaction to Investigate:", display_df['transaction_id'].tolist())
                tx_data = display_df[display_df['transaction_id'] == selected_tx_id].iloc[0]
                
                st.write("**Transaction Details**")
                st.write(f"- **User:** {tx_data['user_id']}")
                st.write(f"- **Amount:** ${tx_data['amount']:,.2f}")
                st.write(f"- **Country:** {tx_data['country']}")
                st.write(f"- **Date:** {tx_data['timestamp']}")
                st.write(f"- **Risk Score:** {tx_data['risk_score']} ({tx_data['risk_label']})")
                
                if st.button("Generate AI Explanation & Run Report"):
                    with st.spinner("Generating insights..."):
                        # Parse factors back to list for explainer
                        factors = [f.strip() for f in tx_data['risk_factors'].split(';') if f.strip()]
                        
                        explanation = llm_explainer.generate_explanation(
                            tx_data.to_dict(), 
                            tx_data['risk_score'], 
                            factors
                        )
                        
                        # Generate Reports
                        txt_path = report_generator.generate_text_sar(tx_data.to_dict(), explanation)
                        pdf_path = report_generator.generate_pdf_sar(tx_data.to_dict(), explanation)
                        
                        st.session_state['current_explanation'] = explanation
                        st.session_state['current_pdf'] = pdf_path
                        st.session_state['current_txt'] = txt_path
                        
            with col_b:
                if 'current_explanation' in st.session_state:
                    st.markdown("### 🤖 Analyst Summary (AI)")
                    st.info(st.session_state['current_explanation'])
                    
                    st.markdown("### 📄 Export Suspicious Activity Report (SAR)")
                    
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        with open(st.session_state['current_pdf'], "rb") as pdf_file:
                            st.download_button("Download PDF SAR", data=pdf_file, file_name=os.path.basename(st.session_state['current_pdf']), type="primary")
                    with d_col2:
                        with open(st.session_state['current_txt'], "r") as txt_file:
                            st.download_button("Download Text SAR", data=txt_file.read(), file_name=os.path.basename(st.session_state['current_txt']))
                            
    with tab3:
        st.subheader("Crypto Wallet Risk Check")
        st.markdown("Bonus Module: Enter a cryptocurrency wallet address to simulate blockchain risk scoring.")
        
        wallet_input = st.text_input("Wallet Address / Tx Hash:")
        if st.button("Analyze Blockchain Risk"):
            if wallet_input:
                with st.spinner("Querying mock blockchain graph..."):
                    res = blockchain_checker.check_wallet(wallet_input)
                    st.markdown(f"**Risk Score:** {res['score']}/100")
                    
                    if res['score'] >= 75:
                        st.error(f"**Reason:** {res['reason']}")
                    elif res['score'] >= 40:
                        st.warning(f"**Reason:** {res['reason']}")
                    else:
                        st.success(f"**Reason:** {res['reason']}")
            else:
                st.warning("Please enter a wallet address.")
