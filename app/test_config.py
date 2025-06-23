import os

# Set test environment variables
os.environ["OPENAI_API_KEY"] = "sk-test-key-for-development"
os.environ["OPENAI_MODEL"] = "gpt-4"
os.environ["CREDIT_SCORE_API_URL"] = "http://localhost:8000"
os.environ["CREDIT_SCORE_API_KEY"] = "test_api_key"

print("Test environment variables set successfully!") 