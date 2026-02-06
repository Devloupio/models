"""
Configuration loader pour Mail2Tickets
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class Config:
    """Configuration centralisée de l'application"""
    
    # Email Configuration
    EMAIL_PROVIDER: str = os.getenv("EMAIL_PROVIDER", "imap")
    IMAP_HOST: str = os.getenv("IMAP_HOST", "imap.gmail.com")
    IMAP_PORT: int = int(os.getenv("IMAP_PORT", "993"))
    IMAP_USERNAME: str = os.getenv("IMAP_USERNAME", "")
    IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD", "")
    IMAP_USE_SSL: bool = os.getenv("IMAP_USE_SSL", "true").lower() == "true"
    IMAP_FOLDER: str = os.getenv("IMAP_FOLDER", "INBOX")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    OPENAI_TIMEOUT: int = int(os.getenv("OPENAI_TIMEOUT", "30"))
    
    # Embeddings
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    USE_EMBEDDINGS: bool = os.getenv("USE_EMBEDDINGS", "false").lower() == "true"
    
    # NocoDB Configuration
    NOCODB_BASE_URL: str = os.getenv("NOCODB_BASE_URL", "")
    NOCODB_API_TOKEN: str = os.getenv("NOCODB_API_TOKEN", "")
    NOCODB_PROJECT_ID: str = os.getenv("NOCODB_PROJECT_ID", "")
    NOCODB_TABLE_TICKETS: str = os.getenv("NOCODB_TABLE_TICKETS", "tickets")
    NOCODB_TABLE_COMMENTS: str = os.getenv("NOCODB_TABLE_COMMENTS", "ticket_comments")
    NOCODB_TABLE_THREADS: str = os.getenv("NOCODB_TABLE_THREADS", "email_threads")
    NOCODB_TABLE_CLIENTS: str = os.getenv("NOCODB_TABLE_CLIENTS", "clients")
    NOCODB_TABLE_SITES: str = os.getenv("NOCODB_TABLE_SITES", "sites")
    NOCODB_TABLE_CI: str = os.getenv("NOCODB_TABLE_CI", "configuration_items")
    NOCODB_TABLE_CATEGORIES: str = os.getenv("NOCODB_TABLE_CATEGORIES", "categories")
    
    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/mail2tickets.log")
    PROCESSING_INTERVAL: int = int(os.getenv("PROCESSING_INTERVAL", "60"))
    MAX_EMAILS_PER_BATCH: int = int(os.getenv("MAX_EMAILS_PER_BATCH", "10"))
    ENABLE_ASYNC_PROCESSING: bool = os.getenv("ENABLE_ASYNC_PROCESSING", "true").lower() == "true"
    
    # Ticket Configuration
    TICKET_NUMBER_PREFIX: str = os.getenv("TICKET_NUMBER_PREFIX", "TICKET")
    TICKET_DEFAULT_PRIORITY: str = os.getenv("TICKET_DEFAULT_PRIORITY", "medium")
    TICKET_DEFAULT_STATUS: str = os.getenv("TICKET_DEFAULT_STATUS", "new")
    AUTO_ASSIGN_TICKETS: bool = os.getenv("AUTO_ASSIGN_TICKETS", "false").lower() == "true"
    
    # Thread Detection
    THREAD_DETECTION_METHOD: str = os.getenv("THREAD_DETECTION_METHOD", "headers")
    SUBJECT_TAG_PATTERN: str = os.getenv("SUBJECT_TAG_PATTERN", r"\[TICKET-\d+\]")
    THREAD_MATCH_THRESHOLD: float = float(os.getenv("THREAD_MATCH_THRESHOLD", "0.8"))
    
    # AI Classification
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = float(os.getenv("CLASSIFICATION_CONFIDENCE_THRESHOLD", "0.7"))
    AUTO_CATEGORIZE: bool = os.getenv("AUTO_CATEGORIZE", "true").lower() == "true"
    AUTO_PRIORITIZE: bool = os.getenv("AUTO_PRIORITIZE", "true").lower() == "true"
    EXTRACT_ENTITIES: bool = os.getenv("EXTRACT_ENTITIES", "true").lower() == "true"
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")
    ENABLE_AUTHENTICATION: bool = os.getenv("ENABLE_AUTHENTICATION", "true").lower() == "true"
    
    # Development
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TESTING_MODE: bool = os.getenv("TESTING_MODE", "false").lower() == "true"
    MOCK_OPENAI: bool = os.getenv("MOCK_OPENAI", "false").lower() == "true"
    MOCK_NOCODB: bool = os.getenv("MOCK_NOCODB", "false").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """Valide la configuration minimale requise"""
        required = []
        
        if not cls.OPENAI_API_KEY and not cls.MOCK_OPENAI:
            required.append("OPENAI_API_KEY")
        
        if not cls.NOCODB_BASE_URL and not cls.MOCK_NOCODB:
            required.append("NOCODB_BASE_URL")
        
        if not cls.NOCODB_API_TOKEN and not cls.MOCK_NOCODB:
            required.append("NOCODB_API_TOKEN")
        
        if cls.EMAIL_PROVIDER == "imap":
            if not cls.IMAP_HOST:
                required.append("IMAP_HOST")
            if not cls.IMAP_USERNAME:
                required.append("IMAP_USERNAME")
            if not cls.IMAP_PASSWORD:
                required.append("IMAP_PASSWORD")
        
        if required:
            raise ValueError(f"Missing required configuration: {', '.join(required)}")
        
        return True


# Instance globale de configuration
config = Config()
