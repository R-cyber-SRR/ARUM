class Config:
    """Configuration settings for the application"""
    DEBUG = True
    SECRET_KEY = 'your-secret-key-here'
    
    # Database settings
    DATABASE_URL = 'sqlite:///arum.db'
    
    # Media settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size