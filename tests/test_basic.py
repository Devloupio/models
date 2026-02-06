"""
Tests de base pour la structure du projet
"""
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_imports():
    """Test que tous les imports principaux fonctionnent"""
    
    # Models
    from models import Ticket, TicketComment, ParsedEmail, AIEnrichment
    from models import TicketStatus, TicketPriority, TicketCategory
    
    # Utils
    from utils import config, logger, get_logger
    
    print("✓ All imports successful")
    return True


def test_config():
    """Test la configuration"""
    from utils.config import config
    
    assert hasattr(config, 'EMAIL_PROVIDER')
    assert hasattr(config, 'OPENAI_MODEL')
    assert hasattr(config, 'NOCODB_BASE_URL')
    
    print("✓ Configuration object valid")
    return True


def test_models():
    """Test les modèles de données"""
    from models import Ticket, TicketStatus, TicketPriority
    from datetime import datetime
    
    # Créer un ticket de test
    ticket = Ticket(
        ticket_number="TICKET-TEST-001",
        subject="Test Subject",
        description="Test Description",
        status=TicketStatus.NEW,
        priority=TicketPriority.MEDIUM,
        requester_email="test@example.com"
    )
    
    # Vérifier la conversion en dict
    ticket_dict = ticket.to_dict()
    assert ticket_dict['ticket_number'] == "TICKET-TEST-001"
    assert ticket_dict['subject'] == "Test Subject"
    
    print("✓ Models working correctly")
    return True


def test_email_model():
    """Test le modèle d'email"""
    from models import ParsedEmail, EmailAddress
    
    email = ParsedEmail(
        message_id="<test@example.com>",
        subject="Test Email",
        from_address=EmailAddress(email="sender@example.com", name="Sender"),
    )
    
    email_dict = email.to_dict()
    assert email_dict['message_id'] == "<test@example.com>"
    assert email_dict['subject'] == "Test Email"
    
    print("✓ Email model working correctly")
    return True


def main():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("  Mail2Tickets - Basic Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Models", test_models),
        ("Email Model", test_email_model),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            result = test_func()
            results.append((test_name, True, None))
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            results.append((test_name, False, str(e)))
    
    print("\n" + "="*60)
    print("  Test Results")
    print("="*60 + "\n")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, error in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status} - {test_name}")
        if error:
            print(f"         Error: {error}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
