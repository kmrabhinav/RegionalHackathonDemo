"""
Configuration Settings
Contains all environment variables and configuration parameters
"""

import os
from typing import Optional

class Settings:
    """
    Application settings and configuration
    """
    
    def __init__(self):
        # Azure OpenAI Configuration
        self.AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', 'your-azure-openai-api-key')
        self.AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://your-resource.openai.azure.com/')
        self.AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4')
        self.AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'text-embedding-ada-002')
        
        # PostgreSQL Configuration
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
        self.POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
        self.POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE', 'voyage_ai')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
        
        # MongoDB Configuration
        self.MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'voyage_ai_vectors')
        
        # MCP Configuration
        self.MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        
        # Application Settings
        self.APP_NAME = "VoyageAI"
        self.APP_VERSION = "1.0.0"
        self.DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
        
        # Agent Configuration
        self.AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', '30'))  # seconds
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
        
        # RAG Configuration
        self.RAG_TOP_K = int(os.getenv('RAG_TOP_K', '5'))
        self.RAG_SIMILARITY_THRESHOLD = float(os.getenv('RAG_SIMILARITY_THRESHOLD', '0.7'))
        
        # API Rate Limits
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
        
    def get_database_url(self) -> str:
        """Get PostgreSQL connection URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
    
    def get_mongodb_url(self) -> str:
        """Get MongoDB connection URL"""
        return self.MONGODB_URI
    
    def validate_azure_config(self) -> bool:
        """Validate Azure OpenAI configuration"""
        required_fields = [
            self.AZURE_OPENAI_API_KEY,
            self.AZURE_OPENAI_ENDPOINT,
            self.AZURE_OPENAI_DEPLOYMENT_NAME
        ]
        
        return all(field and field != 'your-azure-openai-api-key' for field in required_fields)
    
    def __repr__(self) -> str:
        return f"<Settings app={self.APP_NAME} version={self.APP_VERSION}>"


# Create global settings instance
settings = Settings()
