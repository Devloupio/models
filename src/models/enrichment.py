"""
Modèles pour l'enrichissement IA
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from .ticket import TicketCategory, TicketPriority, UrgencyLevel, ImpactLevel


@dataclass
class AIClassification:
    """Classification d'un email par IA"""
    
    # Classification principale
    category: TicketCategory
    subcategory: Optional[str] = None
    confidence: float = 0.0
    
    # Priorisation
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    impact: ImpactLevel = ImpactLevel.MEDIUM
    priority: TicketPriority = TicketPriority.MEDIUM
    
    # Résumé
    summary: str = ""
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "subcategory": self.subcategory,
            "confidence": self.confidence,
            "urgency": self.urgency.value,
            "impact": self.impact.value,
            "priority": self.priority.value,
            "summary": self.summary,
            "keywords": self.keywords,
        }


@dataclass
class ExtractedEntity:
    """Entité extraite d'un email"""
    
    entity_type: str  # client, site, ci, contact, etc.
    value: str
    confidence: float = 0.0
    context: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "value": self.value,
            "confidence": self.confidence,
            "context": self.context,
        }


@dataclass
class AIEnrichment:
    """Résultat complet de l'enrichissement IA"""
    
    # Classification
    classification: AIClassification
    
    # Entités extraites
    entities: List[ExtractedEntity] = field(default_factory=list)
    
    # Données structurées
    client_name: Optional[str] = None
    client_id: Optional[int] = None
    site_name: Optional[str] = None
    site_id: Optional[int] = None
    ci_name: Optional[str] = None
    ci_id: Optional[int] = None
    
    # Détection de ticket existant
    related_ticket_number: Optional[str] = None
    is_follow_up: bool = False
    
    # Méta
    processing_time_ms: float = 0.0
    model_used: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "classification": self.classification.to_dict(),
            "entities": [e.to_dict() for e in self.entities],
            "client_name": self.client_name,
            "client_id": self.client_id,
            "site_name": self.site_name,
            "site_id": self.site_id,
            "ci_name": self.ci_name,
            "ci_id": self.ci_id,
            "related_ticket_number": self.related_ticket_number,
            "is_follow_up": self.is_follow_up,
            "processing_time_ms": self.processing_time_ms,
            "model_used": self.model_used,
        }
