import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# 1. App Configuration
st.set_page_config(page_title="Device Pricing AI", page_icon="📱", layout="wide")
st.title("📱 Secondary Device Pricing Dashboard")
st.markdown("Upload your formatted purchase history and ask questions in plain English.")

# 2. Secure API Key Input (So you don't expose your key in the code)
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
st.sidebar.markdown("*Your key is secure and resets when the page refreshes.*")

# 3. File Uploader
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=['csv', 'xlsx'])

if uploaded_file is not None and api_key:
    # Read the data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("### 📊 Data Preview")
    st.dataframe(df.head(5)) # Shows the first 5 rows so users know it loaded

    # 4. Initialize the AI
    llm = OpenAI(api_token=api_key)
    # Convert standard dataframe to a PandasAI "Smart" Dataframe
    smart_df = SmartDataframe(df, config={"llm": llm, "enable_cache": False})

    # 5. The Natural Language Search Bar
    st.write("### 🤖 Ask the AI")
    user_query = st.text_input("Example: 'Show me a line chart of the average buy price for Grade B iPhones by date'")
    
    if st.button("Generate Insight"):
        if user_query:
            with st.spinner("Analyzing data and generating chart..."):
                try:
                    # The AI processes the question and generates an answer or chart
                    response = smart_df.chat(user_query)
                    
                    # Display the result (text or image)
                    if isinstance(response, str) and response.endswith(('.png', '.jpg', '.jpeg')):
                        st.image(response) # If it's a saved chart image
                    else:
                        st.write(response) # If it's text or a number
                except Exception as e:
                    st.error(f"An error occurred: {e}. Try rephrasing your question.")
        else:
            st.warning("Please enter a question first.")
elif not api_key:
    st.info("👈 Please enter your API Key in the sidebar to begin.")