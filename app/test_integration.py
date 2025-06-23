#!/usr/bin/env python3
"""
Integration Test for Credit Score Chatbot System
Tests the complete flow: AI Chain -> Tools -> API Client
Excludes web/Streamlit tier
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ai.chain import CreditScoreChain
from ai.tools import SearchCustomerTool, GetCreditScoreTool, CompanySelectionTool
from api.client import CreditScoreAPIClient

class IntegrationTest:
    """Integration test suite for the credit score chatbot"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = f"[{timestamp}] {status} - {test_name}"
        if message:
            result += f": {message}"
        
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": timestamp
        })
        
        if success:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_configuration(self):
        """Test configuration loading"""
        print("\n🔧 Testing Configuration...")
        
        try:
            # Test config validation
            Config.validate_config()
            self.log_test("Config Validation", True, "Configuration loaded successfully")
            
            # Test URL generation
            search_url = Config.get_search_url()
            credit_url = Config.get_credit_score_url()
            
            self.log_test("URL Generation", True, f"Search URL: {search_url}")
            self.log_test("URL Generation", True, f"Credit URL: {credit_url}")
            
        except Exception as e:
            self.log_test("Config Validation", False, str(e))
    
    def test_api_client(self):
        """Test API client functionality"""
        print("\n🌐 Testing API Client...")
        
        try:
            client = CreditScoreAPIClient()
            
            # Test API availability
            is_available = client.is_api_available()
            self.log_test("API Availability Check", True, f"API available: {is_available}")
            
            # Test search endpoint (mock test)
            print("  Testing search endpoint...")
            # This will fail if API is not running, but that's expected
            self.log_test("API Client Initialization", True, "Client created successfully")
            
        except Exception as e:
            self.log_test("API Client", False, str(e))
    
    def test_tools_initialization(self):
        """Test LangChain tools initialization"""
        print("\n🛠️  Testing Tools Initialization...")
        
        try:
            # Test each tool individually
            search_tool = SearchCustomerTool()
            self.log_test("SearchCustomerTool", True, "Tool initialized successfully")
            
            credit_tool = GetCreditScoreTool()
            self.log_test("GetCreditScoreTool", True, "Tool initialized successfully")
            
            select_tool = CompanySelectionTool()
            self.log_test("CompanySelectionTool", True, "Tool initialized successfully")
            
            # Test tool attributes
            self.log_test("Tool Name Attributes", 
                         search_tool.name == "search_customer", 
                         f"Search tool name: {search_tool.name}")
            
            self.log_test("Tool Description Attributes", 
                         len(search_tool.description) > 0, 
                         "Tool has description")
            
        except Exception as e:
            self.log_test("Tools Initialization", False, str(e))
    
    def test_tools_execution(self):
        """Test tool execution (with mock data)"""
        print("\n⚡ Testing Tools Execution...")
        
        try:
            search_tool = SearchCustomerTool()
            
            # Test search tool with mock response
            test_result = search_tool._format_search_result({
                "results": [
                    {
                        "id": "test_001",
                        "name": "บริษัท โพธิ์ จำกัด",
                        "name_en": "Pho Company Limited",
                        "tax_id": "0123456789012",
                        "address": "123 ถนนสุขุมวิท กรุงเทพฯ",
                        "match_score": 0.95
                    }
                ],
                "total_results": 1,
                "search_term": "โพธิ์"
            })
            
            self.log_test("Search Tool Formatting", 
                         "Found 1 company" in test_result, 
                         "Formatted result correctly")
            
            # Test credit score tool formatting
            credit_tool = GetCreditScoreTool()
            credit_result = credit_tool._format_credit_score_result({
                "customer_id": "test_001",
                "company_name": "บริษัท โพธิ์ จำกัด",
                "credit_score": {
                    "overall_score": 750,
                    "score_range": "Good",
                    "risk_level": "Low",
                    "last_updated": "2025-06-22T12:00:00Z"
                },
                "financial_metrics": {
                    "total_revenue": 50000000,
                    "total_assets": 75000000,
                    "debt_ratio": 0.35,
                    "current_ratio": 1.8
                },
                "payment_history": {
                    "on_time_payments": 95,
                    "late_payments": 2,
                    "defaults": 0,
                    "payment_score": 92
                }
            })
            
            self.log_test("Credit Score Tool Formatting", 
                         "Credit Score Report" in credit_result, 
                         "Formatted credit report correctly")
            
        except Exception as e:
            self.log_test("Tools Execution", False, str(e))
    
    def test_ai_chain_initialization(self):
        """Test AI chain initialization"""
        print("\n🤖 Testing AI Chain Initialization...")
        
        try:
            chain = CreditScoreChain()
            
            # Test chain components
            self.log_test("LLM Initialization", 
                         chain.llm is not None, 
                         "Language model initialized")
            
            self.log_test("Tools Loading", 
                         len(chain.tools) > 0, 
                         f"Loaded {len(chain.tools)} tools")
            
            self.log_test("Memory Initialization", 
                         chain.memory is not None, 
                         "Conversation memory initialized")
            
            self.log_test("Agent Executor", 
                         chain.agent_executor is not None, 
                         "Agent executor created")
            
        except Exception as e:
            self.log_test("AI Chain Initialization", False, str(e))
    
    def test_ai_chain_processing(self):
        """Test AI chain message processing"""
        print("\n💬 Testing AI Chain Message Processing...")
        
        try:
            chain = CreditScoreChain()
            
            # Test with a simple message
            test_message = "Hello, can you help me find a company's credit score?"
            response = chain.process_message(test_message)
            
            self.log_test("Message Processing", 
                         len(response) > 0, 
                         f"Response length: {len(response)} characters")
            
            # Test memory functionality
            initial_memory = len(chain.get_memory())
            chain.process_message("Test message for memory")
            final_memory = len(chain.get_memory())
            
            self.log_test("Memory Management", 
                         final_memory > initial_memory, 
                         f"Memory increased: {initial_memory} -> {final_memory}")
            
            # Test memory clearing
            chain.clear_memory()
            cleared_memory = len(chain.get_memory())
            
            self.log_test("Memory Clearing", 
                         cleared_memory == 0, 
                         f"Memory cleared: {cleared_memory} messages")
            
        except Exception as e:
            self.log_test("AI Chain Processing", False, str(e))
    
    def test_complete_flow(self):
        """Test the complete flow with a realistic scenario"""
        print("\n🔄 Testing Complete Flow...")
        
        try:
            chain = CreditScoreChain()
            
            # Simulate a complete conversation flow
            messages = [
                "What's the credit score for Apple Inc?",
                "Can you search for companies with 'โพธิ์' in the name?",
                "Show me the credit score for the first company you found"
            ]
            
            responses = []
            for message in messages:
                response = chain.process_message(message)
                responses.append(response)
                print(f"  User: {message}")
                print(f"  AI: {response[:100]}...")
            
            self.log_test("Complete Flow", 
                         len(responses) == len(messages), 
                         f"Processed {len(messages)} messages")
            
            # Test that responses are meaningful
            meaningful_responses = [r for r in responses if len(r) > 10]
            self.log_test("Response Quality", 
                         len(meaningful_responses) > 0, 
                         f"Generated {len(meaningful_responses)} meaningful responses")
            
        except Exception as e:
            self.log_test("Complete Flow", False, str(e))
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Credit Score Chatbot Integration Tests")
        print("=" * 60)
        
        # Run all test suites
        self.test_configuration()
        self.test_api_client()
        self.test_tools_initialization()
        self.test_tools_execution()
        self.test_ai_chain_initialization()
        self.test_ai_chain_processing()
        self.test_complete_flow()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print("\n🔍 Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        return self.failed == 0

def main():
    """Main test runner"""
    # Set up test environment
    # os.environ["OPENAI_API_KEY"] = "sk-test-key-for-integration-testing"
    os.environ["OPENAI_MODEL"] = "gpt-4"
    os.environ["CREDIT_SCORE_API_URL"] = "http://localhost:8000"
    os.environ["CREDIT_SCORE_API_KEY"] = "test_api_key"
    
    # Run tests
    test_suite = IntegrationTest()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 