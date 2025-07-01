#!/usr/bin/env python3
"""
Test script for the Random Dog MCP Demo
Run this to verify everything works before deploying to Hugging Face
"""

import requests
import json
from app import RandomDogAPI, fetch_random_dog, fetch_multiple_dogs

def test_random_dog_api():
    """Test the RandomDogAPI class"""
    print("🧪 Testing RandomDogAPI class...")
    
    api = RandomDogAPI()
    
    # Test single request
    result = api.get_random_dog()
    print(f"✅ Single request result: {result['success']}")
    
    if result['success']:
        print(f"   URL: {result['url'][:50]}...")
        print(f"   File size: {result['fileSizeBytes']} bytes")
    else:
        print(f"   Error: {result['error']}")
    
    # Test stats
    stats = api.get_stats()
    print(f"✅ Stats generated: {len(stats)} characters")
    
    return result['success']

def test_fetch_functions():
    """Test the main fetch functions"""
    print("\n🧪 Testing fetch functions...")
    
    # Test single dog fetch
    image_url, info, stats = fetch_random_dog()
    print(f"✅ Single fetch: {'Success' if image_url else 'Failed'}")
    
    # Test batch fetch
    batch_info, batch_stats = fetch_multiple_dogs(2)
    print(f"✅ Batch fetch: {'Success' if 'Dog 1' in batch_info else 'Failed'}")
    
    return image_url is not None

def test_api_endpoint():
    """Test the random.dog API directly"""
    print("\n🧪 Testing random.dog API directly...")
    
    try:
        response = requests.get("https://random.dog/woof.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Direct API test: Success")
        print(f"   URL: {data.get('url', 'No URL')[:50]}...")
        print(f"   File size: {data.get('fileSizeBytes', 'Unknown')} bytes")
        
        return True
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🐕 Random Dog MCP Demo - Test Suite")
    print("=" * 50)
    
    tests = [
        ("API Endpoint", test_api_endpoint),
        ("RandomDogAPI Class", test_random_dog_api),
        ("Fetch Functions", test_fetch_functions)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Ready for deployment to Hugging Face! 🚀")
    else:
        print("⚠️  Some tests failed. Check your internet connection and try again.")
    
    return all_passed

if __name__ == "__main__":
    main() 