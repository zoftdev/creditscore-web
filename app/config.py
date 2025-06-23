import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    """Configuration class for the credit score chatbot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Credit Score API Configuration
    CREDIT_SCORE_API_URL = os.getenv("CREDIT_SCORE_API_URL", "http://localhost:8000")
    CREDIT_SCORE_API_KEY = os.getenv("CREDIT_SCORE_API_KEY")
    
    # API Endpoints (can be hardcoded as mentioned in plan)
    SEARCH_CUSTOMER_ENDPOINT = "/search-customer"
    CREDIT_SCORE_ENDPOINT = "/credit-score"
    
    # Application Configuration
    APP_TITLE = "Credit Score AI Assistant"
    APP_ICON = "💰"
    
    # Chat Configuration
    MAX_CONVERSATION_HISTORY = 50
    CHAT_INPUT_PLACEHOLDER = "Ask about a company's credit score..."
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_configs = []
        
        if not cls.OPENAI_API_KEY:
            missing_configs.append("OPENAI_API_KEY")
        
        if not cls.CREDIT_SCORE_API_URL:
            missing_configs.append("CREDIT_SCORE_API_URL")
        
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
        
        return True
    
    @classmethod
    def get_search_url(cls):
        """Get the full URL for search customer endpoint"""
        return f"{cls.CREDIT_SCORE_API_URL}{cls.SEARCH_CUSTOMER_ENDPOINT}"
    
    @classmethod
    def get_credit_score_url(cls):
        """Get the full URL for credit score endpoint"""
        return f"{cls.CREDIT_SCORE_API_URL}{cls.CREDIT_SCORE_ENDPOINT}" 