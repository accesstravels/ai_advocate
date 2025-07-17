# PowerShell script to setup environment variables and start the FastAPI server

Write-Host "Setting up Azure AI Avatar Configuration Service..." -ForegroundColor Green
Write-Host ""

# Set Azure Speech Service variables
$env:AZURE_SPEECH_KEY = "your-azure-speech-key-here"
$env:AZURE_SPEECH_REGION = "eastus2"

# Set Azure OpenAI Service variables  
$env:AZURE_OPENAI_KEY = "your-azure-openai-key-here"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4o"

# Set System Prompt
$env:AZURE_SYSTEM_PROMPT = "ты онлайн ассистент юридической консультации и фирмы Владимира Миллера, ты помогаешь людям с их юридическими вопросами, ты жизнерадостный, веселый, дружественный и лояльный, но твоя главная цель это ответив на два три вопроса в чате привлечь как профессиональный маркетолог и агент по продажам на платную юридическую консультацию."

# Set Azure Cognitive Search variables (optional)
$env:AZURE_SEARCH_ENDPOINT = "https://your-search-service.search.windows.net"
$env:AZURE_SEARCH_API_KEY = "your-search-api-key-here"
$env:AZURE_SEARCH_INDEX_NAME = "your-index-name"

# Set Avatar and Voice configuration
$env:AVATAR_CHARACTER = "meg"
$env:AVATAR_STYLE = "formal"
$env:VOICE_NAME = "ru-RU-DmitryNeural"
$env:STT_LOCALE = "ru-RU"

# Optional: Set custom port
$env:PORT = "8000"

Write-Host "Environment variables set successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow

# Start the FastAPI server
python main.py
