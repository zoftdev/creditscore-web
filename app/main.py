import streamlit as st
import os
from config import Config
from ai.chain import CreditScoreChain
from api.client import CreditScoreAPIClient

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide"
)

# Initialize session state
if "credit_score_chain" not in st.session_state:
    st.session_state.credit_score_chain = None
if "api_client" not in st.session_state:
    st.session_state.api_client = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_components():
    """Initialize LangChain and API components"""
    try:
        # Validate configuration
        Config.validate_config()
        
        # Initialize API client
        if st.session_state.api_client is None:
            st.session_state.api_client = CreditScoreAPIClient()
        
        # Initialize LangChain
        if st.session_state.credit_score_chain is None:
            st.session_state.credit_score_chain = CreditScoreChain()
        
        return True
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.info("Please check your .env file and ensure all required environment variables are set.")
        return False
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        return False

def main():
    """Main application function"""
    
    # Header
    st.title(f"{Config.APP_ICON} {Config.APP_TITLE}")
    st.markdown("Ask me about any company's credit score and I'll help you find the information you need.")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # API Status
        if st.session_state.api_client:
            api_status = "🟢 Available" if st.session_state.api_client.is_api_available() else "🔴 Unavailable"
            st.info(f"API Status: {api_status}")
        
        # Clear conversation button
        if st.button("Clear Conversation"):
            if st.session_state.credit_score_chain:
                st.session_state.credit_score_chain.clear_memory()
            st.session_state.messages = []
            st.rerun()
        
        # Configuration info
        st.header("Configuration")
        st.text(f"API URL: {Config.CREDIT_SCORE_API_URL}")
        st.text(f"Model: {Config.OPENAI_MODEL}")
    
    # Initialize components
    if not initialize_components():
        st.stop()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(Config.CHAT_INPUT_PLACEHOLDER):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                try:
                    response = st.session_state.credit_score_chain.process_message(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"I apologize, but I encountered an error: {str(e)}. Please try again."
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main() 