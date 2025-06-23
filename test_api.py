import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("CREDIT_SCORE_API_URL", "http://localhost:8000")
SEARCH_ENDPOINT = "/search-customer"
CREDIT_SCORE_ENDPOINT = "/credit-score"  # Assuming this endpoint exists

def test_search_customer(name):
    """Test the search customer endpoint"""
    url = f"{API_BASE_URL}{SEARCH_ENDPOINT}"
    
    print(f"🔍 Testing search for customer: '{name}'")
    print(f"📡 URL: {url}")
    
    try:
        # Test with different payload formats
        payloads = [
            {"name": name},
            {"query": name},
            {"search_term": name},
            {"customer_name": name}
        ]
        
        for i, payload in enumerate(payloads, 1):
            print(f"\n--- Test {i}: {payload} ---")
            response = requests.post(url, json=payload, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Success! Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    return data
                except json.JSONDecodeError:
                    print(f"⚠️  Response is not JSON: {response.text}")
            else:
                print(f"❌ Error: {response.text}")
        
        # Try GET request as fallback
        print(f"\n--- Test GET request ---")
        response = requests.get(f"{url}?name={name}", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success! Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return data
            except json.JSONDecodeError:
                print(f"⚠️  Response is not JSON: {response.text}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    return None

def test_get_credit_score(customer_id):
    """Test the get credit score endpoint"""
    url = f"{API_BASE_URL}{CREDIT_SCORE_ENDPOINT}"
    
    print(f"\n💰 Testing credit score for customer ID: {customer_id}")
    print(f"📡 URL: {url}")
    
    try:
        # Test with different payload formats
        payloads = [
            {"customer_id": customer_id},
            {"id": customer_id},
            {"customerId": customer_id}
        ]
        
        for i, payload in enumerate(payloads, 1):
            print(f"\n--- Test {i}: {payload} ---")
            response = requests.post(url, json=payload, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Success! Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    return data
                except json.JSONDecodeError:
                    print(f"⚠️  Response is not JSON: {response.text}")
            else:
                print(f"❌ Error: {response.text}")
        
        # Try GET request as fallback
        print(f"\n--- Test GET request ---")
        response = requests.get(f"{url}?customer_id={customer_id}", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success! Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return data
            except json.JSONDecodeError:
                print(f"⚠️  Response is not JSON: {response.text}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    return None

def test_api_health():
    """Test if the API is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"🏥 Health check: {response.status_code}")
        return response.status_code == 200
    except:
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            print(f"🏥 Root endpoint: {response.status_code}")
            return response.status_code == 200
        except:
            print("❌ API is not reachable")
            return False

def main():
    """Main test function"""
    print("🚀 Starting API Tests")
    print(f"📍 API Base URL: {API_BASE_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test API health first
    if not test_api_health():
        print("❌ API is not available. Please check if the service is running.")
        return
    
    # Test search with Thai name
    search_name = "โพธิ์"
    search_result = test_search_customer(search_name)
    
    # If search successful, test getting credit score
    if search_result:
        # Try to extract customer ID from different possible response formats
        customer_id = None
        
        if isinstance(search_result, list) and len(search_result) > 0:
            # If it's a list, take the first result
            first_result = search_result[0]
            customer_id = first_result.get('id') or first_result.get('customer_id') or first_result.get('customerId')
        elif isinstance(search_result, dict):
            # If it's a dict, look for id fields
            customer_id = search_result.get('id') or search_result.get('customer_id') or search_result.get('customerId')
            
            # If no direct id, check if there's a results array
            if not customer_id and 'results' in search_result:
                results = search_result['results']
                if isinstance(results, list) and len(results) > 0:
                    customer_id = results[0].get('id') or results[0].get('customer_id') or results[0].get('customerId')
        
        if customer_id:
            print(f"\n🎯 Found customer ID: {customer_id}")
            credit_score_result = test_get_credit_score(customer_id)
        else:
            print(f"\n⚠️  Could not extract customer ID from search result")
            print(f"Search result structure: {type(search_result)}")
            print(f"Search result content: {search_result}")
    else:
        print(f"\n❌ Search failed for name: {search_name}")

if __name__ == "__main__":
    main() 