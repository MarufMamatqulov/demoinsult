# deployment_helpers.py - will be imported by main.py
import os
import logging

def configure_for_production():
    """Configure application for production environment"""
    logging.info("Configuring application for production environment")
    
    # Set production flag
    os.environ["PRODUCTION"] = "true"
    
    # Check if running on Render.com or similar platforms
    if "RENDER" in os.environ:
        logging.info("Running on Render.com")
        
        # On Render.com, the port is provided as an environment variable
        port = os.environ.get("PORT", 8000)
        os.environ["API_PORT"] = str(port)
        
        # Get the service URL (assigned by Render)
        service_url = os.environ.get("RENDER_EXTERNAL_URL")
        if service_url:
            # Strip trailing slash if present
            if service_url.endswith("/"):
                service_url = service_url[:-1]
            
            # Set as allowed origin for CORS
            os.environ["ALLOWED_ORIGINS"] = f"{service_url},{os.environ.get('FRONTEND_URL', '')}"
            logging.info(f"Setting allowed origins: {os.environ['ALLOWED_ORIGINS']}")
    
    # Configure other production settings
    os.environ["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
    
    # Additional security for production
    os.environ["SECURE_COOKIES"] = "true"
    
    return {
        "is_production": True,
        "port": int(os.environ.get("API_PORT", 8000)),
        "host": os.environ.get("API_HOST", "0.0.0.0"),
        "allowed_origins": os.environ.get("ALLOWED_ORIGINS", "*").split(",")
    }
