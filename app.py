import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# 1. App Configuration (Must be the first command)
st.set_page_config(page_title="Device Pricing AI", page_icon="📱", layout="wide")

# ==========================================
# --- THE NEW SECURITY GATE ---
# ==========================================
# Initialize the login state if it doesn't exist yet
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# If the user is NOT logged in, show the login screen
if not st.session_state.authenticated:
    st.title("🔒 Secure Portal Access")
    st.write("Please verify your identity to access secondary device pricing data.")
    
    user_email = st.text_input("Enter your company email address:")
    
    if st.button("Access Dashboard"):
        # Fetch the secret list of emails we saved in Step 1
        allowed_list = st.secrets.get("allowed_emails", [])
        
        if user_email.lower().strip() in [email.lower() for email in allowed_list]:
            st.session_state.authenticated = True
            st.rerun() # Refresh the page to load the actual app
        else:
            st.error("Access Denied. Your email is not authorized to view this data.")
            
    # The st.stop() command is the actual lock. It prevents any code below 
    # from running until the authentication above is successful.
    st.stop() 
# ==========================================


# 2. The Main App (Only runs if authenticated)
st.title("📱 Secondary Device Pricing Dashboard")
st.markdown("Upload your formatted purchase history and ask questions in plain English.")

api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
st.sidebar.markdown("*Your key is secure and resets when the page refreshes.*")

# Add a logout button to the sidebar
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=['csv', 'xlsx'])

if uploaded_file is not None and api_key:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("### 📊 Data Preview")
    st.dataframe(df.head(5))

    llm = OpenAI(api_token=api_key)
    smart_df = SmartDataframe(df, config={"llm": llm, "enable_cache": False})

    st.write("### 🤖 Ask the AI")
    user_query = st.text_input("Example: 'Show me a line chart of the average buy price for Grade B iPhones by date'")
    
    if st.button("Generate Insight"):
        if user_query:
            with st.spinner("Analyzing data and generating chart..."):
                try:
                    response = smart_df.chat(user_query)
                    if isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg')):
                        st.image(response)
                    else:
                        st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {e}. Try rephrasing your question.")
        else:
            st.warning("Please enter a question first.")
elif not api_key:
    st.info("👈 Please enter your API Key in the sidebar to begin.")
