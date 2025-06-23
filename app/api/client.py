import httpx
import json
from typing import Dict, List, Optional, Any
from config import Config

class CreditScoreAPIClient:
    """Client for interacting with the Credit Score API"""
    
    def __init__(self):
        self.base_url = Config.CREDIT_SCORE_API_URL
        self.api_key = Config.CREDIT_SCORE_API_KEY
        self.timeout = 30.0
        
        # Set up headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    async def search_customer(self, name: str) -> Dict[str, Any]:
        """
        Search for customers by name using fuzzy matching
        
        Args:
            name: Company name to search for
            
        Returns:
            Dictionary containing search results
        """
        url = f"{self.base_url}/search-customer"
        params = {"quote": name}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    url,
                    params=params,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    results = response.json()
                    return {
                        "results": results,
                        "total_results": len(results),
                        "search_term": name
                    }
                else:
                    return {
                        "error": f"API request failed with status {response.status_code}",
                        "details": response.text,
                        "results": []
                    }
                    
        except httpx.TimeoutException:
            return {
                "error": "Request timed out",
                "details": "The API request took too long to complete",
                "results": []
            }
        except httpx.RequestError as e:
            return {
                "error": "Request failed",
                "details": str(e),
                "results": []
            }
        except Exception as e:
            return {
                "error": "Unexpected error",
                "details": str(e),
                "results": []
            }
    
    async def get_credit_score(self, customer_id: str) -> Dict[str, Any]:
        """
        Get credit score information for a specific customer
        
        Args:
            customer_id: The customer ID (account_no) to get credit score for
            
        Returns:
            Dictionary containing credit score information
        """
        url = f"{self.base_url}/query-credit-score"
        params = {"account_no": customer_id}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    url,
                    params=params,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "error": f"API request failed with status {response.status_code}",
                        "details": response.text
                    }
                    
        except httpx.TimeoutException:
            return {
                "error": "Request timed out",
                "details": "The API request took too long to complete"
            }
        except httpx.RequestError as e:
            return {
                "error": "Request failed",
                "details": str(e)
            }
        except Exception as e:
            return {
                "error": "Unexpected error",
                "details": str(e)
            }
    
    def is_api_available(self) -> bool:
        """
        Check if the API is available by making a simple request
        
        Returns:
            True if API is available, False otherwise
        """
        try:
            import requests
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False 