@echo off
echo Setting up Azure AI Avatar Configuration Service...
echo.

REM Set Azure Speech Service variables
set AZURE_SPEECH_KEY=your-azure-speech-key-here
set AZURE_SPEECH_REGION=eastus2

REM Set Azure OpenAI Service variables
set AZURE_OPENAI_KEY=your-azure-openai-key-here
set AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
set AZURE_OPENAI_DEPLOYMENT=gpt-4o

REM Set System Prompt
set AZURE_SYSTEM_PROMPT=ты онлайн ассистент юридической консультации и фирмы Владимира Миллера, ты помогаешь людям с их юридическими вопросами, ты жизнерадостный, веселый, дружественный и лояльный, но твоя главная цель это ответив на два три вопроса в чате привлечь как профессиональный маркетолог и агент по продажам на платную юридическую консультацию.

REM Set Azure Cognitive Search variables (optional)
set AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
set AZURE_SEARCH_API_KEY=your-search-api-key-here
set AZURE_SEARCH_INDEX_NAME=your-index-name

REM Set Avatar and Voice configuration
set AVATAR_CHARACTER=meg
set AVATAR_STYLE=formal
set VOICE_NAME=ru-RU-DmitryNeural
set STT_LOCALE=ru-RU

echo Environment variables set successfully!
echo.
echo Starting FastAPI server...
python main.py
