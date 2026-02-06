"""
Modèles de données
"""
from .email import ParsedEmail, EmailAddress, EmailAttachment, EmailThread
from .ticket import Ticket, TicketComment, TicketStatus, TicketPriority, TicketCategory
from .enrichment import AIEnrichment, AIClassification, ExtractedEntity

__all__ = [
    "ParsedEmail",
    "EmailAddress", 
    "EmailAttachment",
    "EmailThread",
    "Ticket",
    "TicketComment",
    "TicketStatus",
    "TicketPriority",
    "TicketCategory",
    "AIEnrichment",
    "AIClassification",
    "ExtractedEntity",
]
