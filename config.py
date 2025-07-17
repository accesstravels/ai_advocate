"""
Production configuration for Azure AI Avatar Configuration Service.

This module contains production-specific settings and configurations
for deployment to Azure Web App or other production environments.
"""

import os
from typing import List

class ProductionConfig:
    """Production configuration settings."""
    
    # CORS settings for production
    CORS_ORIGINS: List[str] = [
        "https://your-domain.com",  # Replace with your actual domain
        "https://www.your-domain.com",
        "https://your-app.azurewebsites.net"  # Replace with your Azure Web App URL
    ]
    
    # In production, you might want to be more restrictive
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Logging configuration for production
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.environ.get("PORT", 8000))
    
    # Security headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

class DevelopmentConfig:
    """Development configuration settings."""
    
    # More permissive CORS for development
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Debug logging for development
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()
