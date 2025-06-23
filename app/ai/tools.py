from langchain.tools import BaseTool
from typing import Dict, Any, List, Optional
import asyncio
from api.client import CreditScoreAPIClient

# Global API client instance
_api_client = None

def get_api_client():
    """Get or create the API client instance"""
    global _api_client
    if _api_client is None:
        _api_client = CreditScoreAPIClient()
    return _api_client

class SearchCustomerTool(BaseTool):
    """Tool for searching customers by name"""
    
    name: str = "search_customer"
    description: str = "Search for customers/companies by name using fuzzy matching. Use this when a user asks for a company's credit score but you need to find the company first."
    
    def _run(self, name: str) -> str:
        """Run the tool synchronously"""
        try:
            api_client = get_api_client()
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(api_client.search_customer(name))
            loop.close()
            return self._format_search_result(result)
        except Exception as e:
            return f"Error searching for customer '{name}': {str(e)}"
    
    def _format_search_result(self, result: Dict[str, Any]) -> str:
        """Format the search result for the AI"""
        if "error" in result:
            return f"Search failed: {result['error']} - {result.get('details', 'No details available')}"
        
        results = result.get("results", [])
        if not results:
            return f"No companies found matching '{result.get('search_term', 'the search term')}'"
        
        if len(results) == 1:
            company = results[0]
            return f"Found 1 company: {company.get('varname', 'Unknown')} (Account: {company.get('account_no', 'Unknown')}) - Match Score: {company.get('score', 'N/A')}%"
        
        # Multiple results
        formatted_results = []
        for i, company in enumerate(results[:5], 1):  # Limit to top 5
            formatted_results.append(
                f"{i}. {company.get('varname', 'Unknown')} (Account: {company.get('account_no', 'Unknown')}) - Match Score: {company.get('score', 'N/A')}%"
            )
        
        return f"Found {len(results)} companies matching '{result.get('search_term', 'the search term')}':\n" + "\n".join(formatted_results)

class GetCreditScoreTool(BaseTool):
    """Tool for getting credit score information"""
    
    name: str = "get_credit_score"
    description: str = "Get detailed credit score information for a specific customer ID. Use this after finding the correct customer with search_customer tool."
    
    def _run(self, customer_id: str) -> str:
        """Run the tool synchronously"""
        try:
            api_client = get_api_client()
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(api_client.get_credit_score(customer_id))
            loop.close()
            return self._format_credit_score_result(result)
        except Exception as e:
            return f"Error getting credit score for customer ID '{customer_id}': {str(e)}"
    
    def _format_credit_score_result(self, result: Dict[str, Any]) -> str:
        """Format the credit score result for the AI"""
        if "error" in result:
            return f"Credit score retrieval failed: {result['error']} - {result.get('details', 'No details available')}"
        
        # Handle the new API response format
        status = result.get("status", "Unknown")
        message = result.get("message", "")
        company_name = result.get("company_name", "Unknown Company")
        account_no = result.get("account_no", "Unknown")
        credit_score = result.get("credit_score", 0)
        risk_level = result.get("risk_level", "Unknown")
        description = result.get("description", "")
        recommendation = result.get("recommendation", "")
        components = result.get("components", {})
        flags = result.get("flags", {})
        calculation_time = result.get("calculation_time_ms", 0)
        
        # Format the response
        response_parts = [
            f"Credit Score Report for: {company_name}",
            f"Account Number: {account_no}",
            f"Status: {status}",
            f"",
            f"Overall Credit Score: {credit_score}",
            f"Risk Level: {risk_level}",
            f"Description: {description}",
            f"Recommendation: {recommendation}",
            f"Calculation Time: {calculation_time}ms",
            f""
        ]
        
        if components:
            response_parts.extend([
                f"Score Components:",
                *[f"- {key}: {value}" for key, value in components.items()]
            ])
        
        if flags:
            response_parts.extend([
                f"",
                f"Flags:",
                *[f"- {key}: {value}" for key, value in flags.items()]
            ])
        
        return "\n".join(response_parts)

class CompanySelectionTool(BaseTool):
    """Tool for helping users select the correct company when multiple matches are found"""
    
    name: str = "select_company"
    description: str = "Help user select the correct company from multiple search results. Use this when search_customer returns multiple companies."
    
    def _run(self, company_list: str) -> str:
        """Run the tool synchronously"""
        return f"Multiple companies found. Please select the correct one from the list above. You can specify the company name or number to proceed with the credit score analysis." 