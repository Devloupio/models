"""
Logger configuré pour Mail2Tickets
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from .config import config


def setup_logger(
    name: str = "mail2tickets",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Chemin du fichier de log (optionnel)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Définir le niveau
    log_level = level or config.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Éviter les doublons de handlers
    if logger.handlers:
        return logger
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour fichier (si spécifié)
    file_path = log_file or config.LOG_FILE
    if file_path:
        # Créer le répertoire si nécessaire
        log_path = Path(file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger par défaut
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Récupère un logger pour un module spécifique
    
    Args:
        name: Nom du module
    
    Returns:
        Logger configuré
    """
    return setup_logger(f"mail2tickets.{name}")
