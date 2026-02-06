"""
Modèles de données pour Mail2Tickets
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class TicketStatus(str, Enum):
    """Statuts possibles d'un ticket"""
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"


class TicketPriority(str, Enum):
    """Niveaux de priorité d'un ticket"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, Enum):
    """Catégories principales de tickets"""
    INCIDENT = "incident"
    REQUEST = "request"
    CHANGE = "change"
    PROBLEM = "problem"


class UrgencyLevel(str, Enum):
    """Niveaux d'urgence"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ImpactLevel(str, Enum):
    """Niveaux d'impact"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Ticket:
    """Représentation d'un ticket"""
    
    # Identifiants
    id: Optional[int] = None
    ticket_number: Optional[str] = None
    
    # Informations principales
    subject: str = ""
    description: str = ""
    status: TicketStatus = TicketStatus.NEW
    priority: TicketPriority = TicketPriority.MEDIUM
    category: Optional[str] = None
    subcategory: Optional[str] = None
    
    # Demandeur
    requester_email: str = ""
    requester_name: Optional[str] = None
    
    # Assignation
    assigned_to: Optional[str] = None
    
    # Références
    client_id: Optional[int] = None
    site_id: Optional[int] = None
    ci_id: Optional[int] = None
    
    # Urgence et impact
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    impact: ImpactLevel = ImpactLevel.MEDIUM
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    # Métadonnées
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le ticket en dictionnaire"""
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "subject": self.subject,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "category": self.category,
            "subcategory": self.subcategory,
            "requester_email": self.requester_email,
            "requester_name": self.requester_name,
            "assigned_to": self.assigned_to,
            "client_id": self.client_id,
            "site_id": self.site_id,
            "ci_id": self.ci_id,
            "urgency": self.urgency.value,
            "impact": self.impact.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "metadata": self.metadata,
        }


@dataclass
class TicketComment:
    """Commentaire sur un ticket"""
    
    id: Optional[int] = None
    ticket_id: int = 0
    comment_text: str = ""
    author_email: str = ""
    author_name: Optional[str] = None
    is_internal: bool = False
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le commentaire en dictionnaire"""
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "comment_text": self.comment_text,
            "author_email": self.author_email,
            "author_name": self.author_name,
            "is_internal": self.is_internal,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
