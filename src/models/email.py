"""
Modèles de données pour les emails
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class EmailAddress:
    """Représentation d'une adresse email"""
    email: str
    name: Optional[str] = None
    
    def __str__(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email


@dataclass
class EmailAttachment:
    """Représentation d'une pièce jointe"""
    filename: str
    content_type: str
    size: int
    content: Optional[bytes] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size,
        }


@dataclass
class ParsedEmail:
    """Email parsé et nettoyé"""
    
    # Headers
    message_id: str
    subject: str
    from_address: EmailAddress
    to_addresses: List[EmailAddress] = field(default_factory=list)
    cc_addresses: List[EmailAddress] = field(default_factory=list)
    
    # Thread tracking
    in_reply_to: Optional[str] = None
    references: List[str] = field(default_factory=list)
    thread_id: Optional[str] = None
    
    # Contenu
    text_content: str = ""
    html_content: str = ""
    cleaned_content: str = ""  # Nettoyé des signatures, citations, etc.
    
    # Pièces jointes
    attachments: List[EmailAttachment] = field(default_factory=list)
    
    # Métadonnées
    received_at: Optional[datetime] = None
    raw_headers: Dict[str, str] = field(default_factory=dict)
    
    # Détection de ticket existant (à partir du sujet ou corps)
    detected_ticket_number: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'email en dictionnaire"""
        return {
            "message_id": self.message_id,
            "subject": self.subject,
            "from": str(self.from_address),
            "to": [str(addr) for addr in self.to_addresses],
            "cc": [str(addr) for addr in self.cc_addresses],
            "in_reply_to": self.in_reply_to,
            "references": self.references,
            "thread_id": self.thread_id,
            "text_content": self.text_content,
            "html_content": self.html_content,
            "cleaned_content": self.cleaned_content,
            "attachments": [att.to_dict() for att in self.attachments],
            "received_at": self.received_at.isoformat() if self.received_at else None,
            "detected_ticket_number": self.detected_ticket_number,
        }


@dataclass
class EmailThread:
    """Thread d'emails lié à un ticket"""
    
    id: Optional[int] = None
    ticket_id: Optional[int] = None
    message_id: str = ""
    in_reply_to: Optional[str] = None
    references: str = ""  # JSON array as string
    thread_id: str = ""
    subject: str = ""
    from_email: str = ""
    to_emails: str = ""  # JSON array as string
    cc_emails: str = ""  # JSON array as string
    received_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le thread en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "message_id": self.message_id,
            "in_reply_to": self.in_reply_to,
            "references": self.references,
            "thread_id": self.thread_id,
            "subject": self.subject,
            "from_email": self.from_email,
            "to_emails": self.to_emails,
            "cc_emails": self.cc_emails,
            "received_at": self.received_at.isoformat() if self.received_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }
