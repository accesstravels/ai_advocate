#!/usr/bin/env python3
"""
Test script for Azure App Service deployment
"""
import os
import sys

def test_environment():
    """Test that all required environment variables are set"""
    required_vars = [
        'AZURE_OPENAI_KEY',
        'AZURE_OPENAI_ENDPOINT', 
        'AZURE_OPENAI_DEPLOYMENT',
        'AZURE_SEARCH_ENDPOINT',
        'AZURE_SEARCH_API_KEY',
        'AZURE_SEARCH_INDEX_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import pydantic
        import aiohttp
        from config import get_config
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config import get_config
        config = get_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   - Host: {config.HOST}")
        print(f"   - Port: {config.PORT}")
        print(f"   - Log Level: {config.LOG_LEVEL}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Azure App Service deployment...")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment),
        ("Module Imports", test_imports),
        ("Configuration", test_config)
    ]
    
    all_passed = True
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! Ready for Azure deployment.")
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        sys.exit(1)
