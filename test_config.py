"""Test configuration loading"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Environment variables loaded from .env:")
vars_to_check = [
    "AZURE_SPEECH_KEY",
    "AZURE_SPEECH_REGION", 
    "AZURE_OPENAI_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_API_KEY",
    "AZURE_SEARCH_INDEX_NAME",
    "AZURE_SYSTEM_PROMPT",
    "AVATAR_CHARACTER",
    "AVATAR_STYLE",
    "VOICE_NAME",
    "STT_LOCALE"
]

for var in vars_to_check:
    value = os.environ.get(var)
    print(f"{var}: {'SET' if value and value.strip() else 'EMPTY'}")
    
print("\nTesting config.py:")
from config import get_config

config = get_config()
print(f"Config type: {type(config)}")
print(f"Config attributes: {dir(config)}")

# Test Azure OpenAI config
print(f"\nAzure OpenAI config:")
print(f"AZURE_OPENAI_KEY: {'SET' if hasattr(config, 'AZURE_OPENAI_KEY') and config.AZURE_OPENAI_KEY and config.AZURE_OPENAI_KEY.strip() else 'EMPTY'}")
print(f"AZURE_OPENAI_ENDPOINT: {'SET' if hasattr(config, 'AZURE_OPENAI_ENDPOINT') and config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_ENDPOINT.strip() else 'EMPTY'}")
print(f"AZURE_OPENAI_DEPLOYMENT: {'SET' if hasattr(config, 'AZURE_OPENAI_DEPLOYMENT') and config.AZURE_OPENAI_DEPLOYMENT and config.AZURE_OPENAI_DEPLOYMENT.strip() else 'EMPTY'}")
