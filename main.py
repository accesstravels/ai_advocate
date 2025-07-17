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
from pydantic import BaseModel
from config import get_config

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

@app.get("/debug-avatar")
async def debug_avatar_page():
    """Serve avatar debug page."""
    return FileResponse("avatar-debug.html")

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
        
        logger.info(f"Starting Azure AI Avatar Configuration Service on port {port}")
        
        # Run the application
        uvicorn.run(
            "main:app",
            host=config.HOST,
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
