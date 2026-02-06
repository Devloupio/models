"""
Mail2Tickets - Point d'entrée principal

Ce module orchestre le pipeline complet:
1. Ingestion des emails
2. Parsing et nettoyage
3. Enrichissement IA
4. Matching de tickets
5. Persistance dans NocoDB
"""
import sys
import time
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import config
from utils.logger import get_logger

logger = get_logger("main")


def validate_configuration():
    """Valide la configuration avant de démarrer"""
    logger.info("Validating configuration...")
    
    try:
        config.validate()
        logger.info("✓ Configuration validated successfully")
        return True
    except ValueError as e:
        logger.error(f"✗ Configuration validation failed: {e}")
        logger.error("Please check your .env file and ensure all required variables are set")
        return False


def display_banner():
    """Affiche la bannière de démarrage"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║              📧 Mail2Tickets System 🎫                   ║
    ║                                                          ║
    ║     Intelligent Email-to-Ticket Conversion System       ║
    ║           Powered by OpenAI & NocoDB                    ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_status():
    """Affiche le statut de la configuration"""
    print("\n📋 Configuration Status:")
    print(f"  • Email Provider: {config.EMAIL_PROVIDER}")
    print(f"  • OpenAI Model: {config.OPENAI_MODEL}")
    print(f"  • NocoDB URL: {config.NOCODB_BASE_URL}")
    print(f"  • Log Level: {config.LOG_LEVEL}")
    print(f"  • Processing Interval: {config.PROCESSING_INTERVAL}s")
    print(f"  • Debug Mode: {config.DEBUG}")
    print()


def main():
    """Fonction principale"""
    
    # Afficher la bannière
    display_banner()
    
    # Valider la configuration
    if not validate_configuration():
        logger.error("Cannot start application due to configuration errors")
        sys.exit(1)
    
    # Afficher le statut
    display_status()
    
    logger.info("Starting Mail2Tickets application...")
    
    # TODO: Implémenter le pipeline complet
    # Pour l'instant, c'est un placeholder qui montre la structure
    
    logger.warning("⚠️  Pipeline not yet fully implemented")
    logger.info("This is a MVP structure. Next steps:")
    logger.info("  1. Implement email ingestion service")
    logger.info("  2. Implement email parser")
    logger.info("  3. Implement AI enrichment service")
    logger.info("  4. Implement ticket matcher")
    logger.info("  5. Implement NocoDB client")
    
    # Mode démo
    if config.TESTING_MODE:
        logger.info("Running in TESTING_MODE - simulating pipeline...")
        demo_pipeline()
    else:
        logger.info("Application ready. Waiting for implementation...")
        
        # Boucle principale (pour l'instant juste un placeholder)
        try:
            while True:
                logger.info(f"Checking for new emails... (interval: {config.PROCESSING_INTERVAL}s)")
                time.sleep(config.PROCESSING_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Shutting down gracefully...")
            sys.exit(0)


def demo_pipeline():
    """Pipeline de démonstration pour tester la structure"""
    logger.info("="*60)
    logger.info("DEMO PIPELINE")
    logger.info("="*60)
    
    # Simuler les étapes
    steps = [
        ("📨 Email Ingestion", "Fetching emails from IMAP server"),
        ("🔍 Email Parsing", "Parsing and cleaning email content"),
        ("🤖 AI Enrichment", "Analyzing with OpenAI"),
        ("🎯 Ticket Matching", "Searching for existing tickets"),
        ("💾 Persistence", "Saving to NocoDB"),
    ]
    
    for step_name, step_desc in steps:
        logger.info(f"\n{step_name}")
        logger.info(f"  → {step_desc}")
        time.sleep(1)
    
    logger.info("\n" + "="*60)
    logger.info("DEMO COMPLETED")
    logger.info("="*60)
    
    logger.info("\nTo implement real pipeline, check:")
    logger.info("  • src/services/email_ingestion/")
    logger.info("  • src/services/email_parser/")
    logger.info("  • src/services/ai_enrichment/")
    logger.info("  • src/services/ticket_matcher/")
    logger.info("  • src/services/nocodb_client/")


if __name__ == "__main__":
    main()
