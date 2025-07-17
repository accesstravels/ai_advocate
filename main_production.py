"""
FastAPI application for Azure AI Avatar configuration service.

This application provides a secure configuration endpoint for Azure AI Avatar
frontend applications. It loads configuration from environment variables
and serves them via a REST API endpoint.

Security considerations:
- API keys are loaded from environment variables (never hardcoded)
- CORS is enabled for browser access
- Configuration is served without logging sensitive data
- Production-ready with proper error handling
"""

import os
import logging
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel
from config import get_config
import aiohttp

# Load environment variables from .env file
load_dotenv()

# Get configuration based on environment
config = get_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Azure AI Avatar Configuration Service",
    description="Secure configuration endpoint for Azure AI Avatar applications",
    version="1.0.0"
)

# Add CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

# Mount static files
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/image", StaticFiles(directory="image"), name="image")

# Add security headers middleware (production only)
if hasattr(config, 'SECURITY_HEADERS'):
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        for header, value in config.SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

# Configuration model for response validation
class ConfigurationResponse(BaseModel):
    """Response model for configuration endpoint."""
    azure_speech_key: Optional[str] = None
    azure_speech_region: Optional[str] = None
    azure_openai_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_system_prompt: Optional[str] = None
    azure_search_endpoint: Optional[str] = None
    azure_search_api_key: Optional[str] = None
    azure_search_index_name: Optional[str] = None
    avatar_character: Optional[str] = None
    avatar_style: Optional[str] = None
    voice_name: Optional[str] = None
    stt_locale: Optional[str] = None


# Chat models
class ChatMessage(BaseModel):
    """Model for chat message."""
    role: str
    content: str


class SimpleChatRequest(BaseModel):
    """Model for simple chat request."""
    message: str
    use_search: bool = False


class ChatRequest(BaseModel):
    """Model for chat request."""
    messages: list[ChatMessage]
    stream: bool = False
    max_tokens: int = 500
    temperature: float = 0.7


class ChatResponse(BaseModel):
    """Model for chat response."""
    response: str
    status: str = "success"


def load_configuration() -> Dict[str, Optional[str]]:
    """
    Load configuration from environment variables.
    
    Returns:
        Dict containing configuration values, with None for missing variables.
    
    Security note: This function safely retrieves configuration without
    exposing sensitive data in logs or error messages.
    """
    config = {
        "azure_speech_key": os.environ.get("AZURE_SPEECH_KEY"),
        "azure_speech_region": os.environ.get("AZURE_SPEECH_REGION"),
        "azure_openai_key": os.environ.get("AZURE_OPENAI_KEY"),
        "azure_openai_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
        "azure_openai_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        "azure_system_prompt": os.environ.get("AZURE_SYSTEM_PROMPT"),
        "azure_search_endpoint": os.environ.get("AZURE_SEARCH_ENDPOINT"),
        "azure_search_api_key": os.environ.get("AZURE_SEARCH_API_KEY"),
        "azure_search_index_name": os.environ.get("AZURE_SEARCH_INDEX_NAME"),
        "avatar_character": os.environ.get("AVATAR_CHARACTER"),
        "avatar_style": os.environ.get("AVATAR_STYLE"),
        "voice_name": os.environ.get("VOICE_NAME"),
        "stt_locale": os.environ.get("STT_LOCALE"),
    }
    
    # Log configuration loading status (without exposing sensitive data)
    loaded_count = sum(1 for value in config.values() if value is not None)
    logger.info(f"Configuration loaded: {loaded_count}/{len(config)} environment variables found")
    
    return config


@app.get("/config", response_model=ConfigurationResponse)
async def get_configuration():
    """
    Get application configuration from environment variables.
    
    Returns:
        JSON response containing configuration values.
        
    Raises:
        HTTPException: If configuration loading fails.
        
    Security considerations:
    - API keys are never logged to console
    - Configuration is loaded from environment variables only
    - No sensitive data is exposed in error messages
    - Sensitive keys are masked for security
    """
    try:
        config = load_configuration()
        logger.info("Configuration endpoint accessed successfully")
        
        # SECURITY: Mask sensitive data before returning
        safe_config = {
            "azure_speech_key": "***MASKED***" if config.get("azure_speech_key") else None,
            "azure_speech_region": config.get("azure_speech_region"),
            "azure_openai_key": "***MASKED***" if config.get("azure_openai_key") else None,
            "azure_openai_endpoint": config.get("azure_openai_endpoint"),
            "azure_openai_deployment": config.get("azure_openai_deployment"),
            "azure_system_prompt": config.get("azure_system_prompt"),
            "azure_search_endpoint": config.get("azure_search_endpoint"),
            "azure_search_api_key": "***MASKED***" if config.get("azure_search_api_key") else None,
            "azure_search_index_name": config.get("azure_search_index_name"),
            "avatar_character": config.get("avatar_character"),
            "avatar_style": config.get("avatar_style"),
            "voice_name": config.get("voice_name"),
            "stt_locale": config.get("stt_locale"),
        }
        
        return ConfigurationResponse(**safe_config)
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to load configuration"
        )


@app.get("/internal/config")
async def get_internal_configuration():
    """
    Internal endpoint for frontend to get actual configuration.
    This endpoint should not be publicly accessible.
    
    Returns:
        JSON response containing actual configuration values for frontend use.
    """
    try:
        config = load_configuration()
        logger.info("Internal configuration endpoint accessed")
        return config
    except Exception as e:
        logger.error(f"Failed to load internal configuration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to load configuration"
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment validation.
    
    Returns:
        JSON response indicating service health.
    """
    return {"status": "healthy", "service": "Azure AI Avatar Configuration Service"}


# HTML routes
@app.get("/")
async def root_page():
    """Serve the main auto-start chat page."""
    return FileResponse("chat-auto.html")

@app.get("/chat")
async def chat_page():
    """Serve the chat page with API configuration."""
    return FileResponse("chat-with-api.html")

@app.get("/chat-auto")
async def chat_auto_page():
    """Serve the auto-start chat page."""
    return FileResponse("chat-auto.html")

@app.get("/chat-simple")
async def chat_simple_page():
    """Serve the simple chat page with hardcoded configuration."""
    return FileResponse("chat.html")

@app.get("/test-config")
async def test_config_page():
    """Serve test configuration page."""
    return FileResponse("test-config.html")

@app.get("/test-search")
async def test_search_page():
    """Serve Azure Search test page."""
    return FileResponse("test-search.html")

@app.get("/debug-avatar")
async def debug_avatar_page():
    """Serve avatar debug page."""
    return FileResponse("avatar-debug.html")

@app.get("/test-chat-api")
async def test_chat_api_page():
    """Serve chat API test page."""
    return FileResponse("test-chat-api.html")

@app.get("/test-vector-db")
async def test_vector_db_page():
    """Serve vector database test page."""
    return FileResponse("test-vector-db.html")

@app.get("/test-simple-chat")
async def test_simple_chat():
    """Serve simple chat test page without vector database."""
    return FileResponse("test-simple-chat.html")

@app.get("/test-azure-search")
async def test_azure_search():
    """Serve Azure Search test page."""
    return FileResponse("test-azure-search.html")

@app.get("/info")
async def info():
    """Service information."""
    return {
        "service": "Azure AI Avatar Configuration Service",
        "version": "1.0.0",
        "endpoints": {
            "main": "/ (auto-start chat)",
            "config": "/config",
            "health": "/health",
            "chat": "/chat",
            "test": "/test-config",
            "debug": "/debug-avatar"
        }
    }


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for processing user messages with Azure OpenAI and Azure Search.
    
    Args:
        request: Chat request with messages and parameters
        
    Returns:
        Chat response with AI-generated text from Azure Search knowledge base
    """
    return await process_chat_request(request, use_search=True)


# Simple chat endpoint for testing
@app.post("/simple-chat", response_model=ChatResponse)
async def simple_chat_endpoint(request: SimpleChatRequest):
    """
    Simple chat endpoint for testing Azure Search integration.
    
    Args:
        request: Simple chat request with message and use_search flag
        
    Returns:
        Chat response with AI-generated text
    """
    try:
        logger.info(f"Processing simple chat request: {request.message[:50]}...")
        
        # Create ChatRequest object
        chat_request = ChatRequest(messages=[ChatMessage(role="user", content=request.message)])
        
        # Process the request
        return await process_chat_request(chat_request, request.use_search)
        
    except Exception as e:
        logger.error(f"Error in simple chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


async def process_chat_request(request: ChatRequest, use_search: bool = False):
    """
    Process chat request with Azure OpenAI.
    
    Args:
        request: Chat request with messages and parameters
        use_search: Whether to use Azure Search integration
        
    Returns:
        Chat response with AI-generated text
    """
    try:
        logger.info(f"Processing chat request with {len(request.messages)} messages")
        
        # Validate Azure OpenAI configuration
        logger.info(f"Checking Azure OpenAI configuration...")
        logger.info(f"AZURE_OPENAI_KEY: {'SET' if hasattr(config, 'AZURE_OPENAI_KEY') and config.AZURE_OPENAI_KEY and config.AZURE_OPENAI_KEY.strip() else 'EMPTY'}")
        logger.info(f"AZURE_OPENAI_ENDPOINT: {'SET' if hasattr(config, 'AZURE_OPENAI_ENDPOINT') and config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_ENDPOINT.strip() else 'EMPTY'}")
        logger.info(f"AZURE_OPENAI_DEPLOYMENT: {'SET' if hasattr(config, 'AZURE_OPENAI_DEPLOYMENT') and config.AZURE_OPENAI_DEPLOYMENT and config.AZURE_OPENAI_DEPLOYMENT.strip() else 'EMPTY'}")
        
        if not all([
            hasattr(config, 'AZURE_OPENAI_KEY') and config.AZURE_OPENAI_KEY and config.AZURE_OPENAI_KEY.strip(),
            hasattr(config, 'AZURE_OPENAI_ENDPOINT') and config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_ENDPOINT.strip(),
            hasattr(config, 'AZURE_OPENAI_DEPLOYMENT') and config.AZURE_OPENAI_DEPLOYMENT and config.AZURE_OPENAI_DEPLOYMENT.strip()
        ]):
            logger.error("Azure OpenAI configuration is incomplete")
            raise HTTPException(
                status_code=500,
                detail="Azure OpenAI configuration is incomplete"
            )
        
        # Prepare request body for Azure OpenAI
        request_body = {
            "messages": [{"role": msg.role, "content": msg.content} for msg in request.messages],
            "stream": request.stream,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
        
        # Check if Azure Search is configured and should be used
        use_azure_search = (use_search and 
                           hasattr(config, 'AZURE_SEARCH_ENDPOINT') and config.AZURE_SEARCH_ENDPOINT and 
                           hasattr(config, 'AZURE_SEARCH_API_KEY') and config.AZURE_SEARCH_API_KEY and 
                           hasattr(config, 'AZURE_SEARCH_INDEX_NAME') and config.AZURE_SEARCH_INDEX_NAME)
        
        if use_azure_search:
            logger.info("Adding Azure Search data source")
            # Правильный формат для Azure Search с векторным семантическим поиском
            request_body["data_sources"] = [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": config.AZURE_SEARCH_ENDPOINT,
                    "index_name": config.AZURE_SEARCH_INDEX_NAME,
                    "authentication": {
                        "type": "api_key",
                        "key": config.AZURE_SEARCH_API_KEY
                    },
                    "query_type": "vector_semantic_hybrid",
                    "semantic_configuration": f"{config.AZURE_SEARCH_INDEX_NAME}-semantic-configuration",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": "text-embedding-ada-002"
                    },
                    "in_scope": True,
                    "top_n_documents": 10,
                    "strictness": 2
                }
            }]
        else:
            logger.info("Using standard Azure OpenAI API (without Azure Search)")
            # Добавим системное сообщение в начало
            system_message = {
                "role": "system",
                "content": (config.AZURE_SYSTEM_PROMPT if hasattr(config, 'AZURE_SYSTEM_PROMPT') and config.AZURE_SYSTEM_PROMPT else "Ты юридический помощник фирмы Владимира Миллера.")
            }
            request_body["messages"].insert(0, system_message)
        
        # Make request to Azure OpenAI
        # Используем стандартный API для всех случаев
        api_url = f"{config.AZURE_OPENAI_ENDPOINT}/openai/deployments/{config.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-10-21"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                api_url,
                headers={
                    'api-key': config.AZURE_OPENAI_KEY,
                    'Content-Type': 'application/json'
                },
                json=request_body
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Azure OpenAI API error: {response.status} - {error_text}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Azure OpenAI API error: {error_text}"
                    )
                
                response_data = await response.json()
                
                # Extract response text
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    choice = response_data['choices'][0]
                    
                    # For Azure Search Extensions API, the response might be in a different format
                    if 'message' in choice:
                        ai_response = choice['message']['content']
                        
                        # Log additional info for Azure Search responses
                        if use_azure_search and 'context' in choice.get('message', {}):
                            citations = choice['message'].get('context', {}).get('citations', [])
                            logger.info(f"Azure Search found {len(citations)} citations")
                            
                            # Логируем первые несколько цитат для отладки
                            for i, citation in enumerate(citations[:3]):
                                logger.info(f"Citation {i+1}: {citation.get('content', '')[:100]}...")
                                logger.info(f"Citation {i+1} title: {citation.get('title', 'No title')}")
                            
                            # Проверяем intent
                            context = choice['message'].get('context', {})
                            if 'intent' in context:
                                logger.info(f"Search intent: {context['intent']}")
                            
                            logger.info(f"Full response content: {ai_response[:200]}...")
                            
                    else:
                        # Fallback for other response formats
                        ai_response = choice.get('text', choice.get('content', ''))
                    
                    logger.info(f"Successfully processed chat request. Response length: {len(ai_response)}")
                    return ChatResponse(response=ai_response, status="success")
                else:
                    logger.error("No choices in Azure OpenAI response")
                    raise HTTPException(
                        status_code=500,
                        detail="No response from Azure OpenAI"
                    )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The request object
        exc: The exception that occurred
        
    Returns:
        JSON error response
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    try:
        import uvicorn
        
        # Get port from environment or use config default
        port = int(os.environ.get("PORT", config.PORT))
        
        # For Azure App Service, use host 0.0.0.0
        host = os.environ.get("HOST", config.HOST)
        if host == "127.0.0.1":  # Change localhost to 0.0.0.0 for Azure
            host = "0.0.0.0"
        
        logger.info(f"Starting Azure AI Avatar Configuration Service on {host}:{port}")
        
        # Run the application
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,  # Set to True for development
            log_level=config.LOG_LEVEL.lower()
        )
    except ImportError:
        logger.error("uvicorn is not installed. Please install it with: pip install uvicorn")
        exit(1)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1)
