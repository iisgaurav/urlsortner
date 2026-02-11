"""
Test script to verify URL shortener API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_url():
    """Test creating a short URL."""
    print("\n" + "="*50)
    print("TEST 1: Create Short URL")
    print("="*50)
    
    url = f"{BASE_URL}/api/shorten/"
    data = {
        "original_url": "https://www.google.com"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Short URL created!")
            return response.json()
        else:
            print("❌ FAILED: Unexpected status code")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None


def test_redirect(short_code):
    """Test redirection."""
    print("\n" + "="*50)
    print("TEST 2: Redirect to Original URL")
    print("="*50)
    
    url = f"{BASE_URL}/{short_code}/"
    
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Location: {response.headers.get('Location', 'N/A')}")
        
        if response.status_code == 302:
            print("✅ SUCCESS: Redirect working!")
        else:
            print("❌ FAILED: Expected 302 redirect")
    except Exception as e:
        print(f"❌ ERROR: {e}")


def test_analytics(short_code):
    """Test analytics endpoint."""
    print("\n" + "="*50)
    print("TEST 3: Get Analytics")
    print("="*50)
    
    url = f"{BASE_URL}/api/analytics/{short_code}/"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Analytics retrieved!")
        else:
            print("❌ FAILED: Unexpected status code")
    except Exception as e:
        print(f"❌ ERROR: {e}")


def test_custom_code():
    """Test creating URL with custom code."""
    print("\n" + "="*50)
    print("TEST 4: Create URL with Custom Code")
    print("="*50)
    
    url = f"{BASE_URL}/api/shorten/"
    data = {
        "original_url": "https://github.com",
        "custom_code": "github"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Custom code URL created!")
        else:
            print("❌ FAILED: Unexpected status code")
    except Exception as e:
        print(f"❌ ERROR: {e}")


def test_rate_limiting():
    """Test rate limiting."""
    print("\n" + "="*50)
    print("TEST 5: Rate Limiting (Making 12 requests)")
    print("="*50)
    
    url = f"{BASE_URL}/api/shorten/"
    success_count = 0
    rate_limited_count = 0
    
    for i in range(12):
        data = {
            "original_url": f"https://example{i}.com"
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                success_count += 1
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"  Request {i+1}: Rate limited (429)")
        except Exception as e:
            print(f"  Request {i+1}: Error - {e}")
    
    print(f"\nSuccessful requests: {success_count}")
    print(f"Rate limited requests: {rate_limited_count}")
    
    if rate_limited_count > 0:
        print("✅ SUCCESS: Rate limiting is working!")
    else:
        print("⚠️  WARNING: Rate limiting may not be active")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("URL SHORTENER API TESTS")
    print("="*50)
    
    # Test 1: Create short URL
    result = test_create_url()
    
    if result:
        short_code = result.get('short_url', '').split('/')[-1]
        
        # Test 2: Redirect
        if short_code:
            test_redirect(short_code)
            
            # Test 3: Analytics
            test_analytics(short_code)
    
    # Test 4: Custom code
    test_custom_code()
    
    # Test 5: Rate limiting
    test_rate_limiting()
    
    print("\n" + "="*50)
    print("TESTS COMPLETED")
    print("="*50)
