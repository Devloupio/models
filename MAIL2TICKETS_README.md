# Mail2Tickets - Système de Ticketing Intelligent

## Vue d'ensemble

Mail2Tickets est une solution innovante de gestion de tickets basée sur l'analyse intelligente d'emails via l'IA (OpenAI) et une base de données NocoDB/PostgreSQL.

## Architecture

### Composants Principaux

```
┌─────────────────┐
│  Email Sources  │ (IMAP/POP3/SMTP Webhook)
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Email Ingestion │ Service de réception et normalisation
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Email Parser    │ Nettoyage, extraction headers, corps, PJ
└────────┬────────┘
         │
         v
┌─────────────────┐
│ AI Enrichment   │ OpenAI: classification, extraction, résumé
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Ticket Matcher  │ Recherche ticket existant ou création
└────────┬────────┘
         │
         v
┌─────────────────┐
│ NocoDB API      │ Persistance tickets, commentaires, threads
└─────────────────┘
```

### Flux de Données

1. **Ingestion** : Récupération des emails depuis une ou plusieurs sources
2. **Parsing** : Extraction et nettoyage du contenu (headers, corps, PJ)
3. **Enrichissement IA** : 
   - Classification (incident, demande, changement)
   - Catégorisation automatique
   - Calcul urgence/impact → priorité
   - Extraction données structurées (client, site, CI, etc.)
   - Détection ID ticket existant
4. **Matching** : Interrogation NocoDB pour trouver ticket existant ou créer nouveau
5. **Persistance** : CRUD via API NocoDB

## Schéma de Base de Données

### Tables Principales

#### tickets
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique du ticket |
| ticket_number | VARCHAR UNIQUE | Numéro public (ex: TICKET-1234) |
| status | ENUM | new, assigned, in_progress, resolved, closed |
| priority | ENUM | low, medium, high, critical |
| category | VARCHAR | Catégorie principale |
| subcategory | VARCHAR | Sous-catégorie |
| subject | TEXT | Sujet du ticket |
| description | TEXT | Description complète |
| requester_email | VARCHAR | Email du demandeur |
| requester_name | VARCHAR | Nom du demandeur |
| assigned_to | VARCHAR | Assigné à |
| client_id | INT FK | Référence client |
| site_id | INT FK | Référence site |
| ci_id | INT FK | Référence CI (Configuration Item) |
| urgency | ENUM | low, medium, high |
| impact | ENUM | low, medium, high |
| created_at | TIMESTAMP | Date création |
| updated_at | TIMESTAMP | Date dernière modification |
| resolved_at | TIMESTAMP | Date résolution |
| closed_at | TIMESTAMP | Date fermeture |

#### ticket_comments
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| ticket_id | INT FK | Référence ticket |
| comment_text | TEXT | Contenu du commentaire |
| author_email | VARCHAR | Email auteur |
| author_name | VARCHAR | Nom auteur |
| is_internal | BOOLEAN | Commentaire interne ou public |
| created_at | TIMESTAMP | Date création |

#### email_threads
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| ticket_id | INT FK | Référence ticket |
| message_id | VARCHAR UNIQUE | Message-ID de l'email |
| in_reply_to | VARCHAR | In-Reply-To header |
| references | TEXT | References header |
| thread_id | VARCHAR | ID de thread normalisé |
| subject | TEXT | Sujet email |
| from_email | VARCHAR | Expéditeur |
| to_emails | TEXT | Destinataires |
| cc_emails | TEXT | Copie |
| received_at | TIMESTAMP | Date réception |
| processed_at | TIMESTAMP | Date traitement |

#### clients
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| name | VARCHAR | Nom client |
| email_domain | VARCHAR | Domaine email |
| contact_email | VARCHAR | Email contact |
| phone | VARCHAR | Téléphone |
| sla_level | ENUM | bronze, silver, gold, platinum |

#### sites
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| client_id | INT FK | Référence client |
| name | VARCHAR | Nom du site |
| address | TEXT | Adresse |
| city | VARCHAR | Ville |
| country | VARCHAR | Pays |

#### configuration_items (CI)
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| name | VARCHAR | Nom CI |
| type | VARCHAR | Type (serveur, application, réseau...) |
| site_id | INT FK | Référence site |
| status | ENUM | active, inactive, maintenance |

#### categories
| Champ | Type | Description |
|-------|------|-------------|
| id | INT PK | ID unique |
| name | VARCHAR | Nom catégorie |
| parent_id | INT FK | Catégorie parente (NULL si racine) |
| description | TEXT | Description |

## Structure du Projet

```
mail2tickets/
├── src/
│   ├── services/
│   │   ├── email_ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── imap_client.py
│   │   │   ├── pop3_client.py
│   │   │   └── smtp_webhook.py
│   │   ├── email_parser/
│   │   │   ├── __init__.py
│   │   │   ├── parser.py
│   │   │   ├── cleaner.py
│   │   │   └── thread_detector.py
│   │   ├── ai_enrichment/
│   │   │   ├── __init__.py
│   │   │   ├── openai_client.py
│   │   │   ├── classifier.py
│   │   │   ├── extractor.py
│   │   │   └── prompts.py
│   │   ├── ticket_matcher/
│   │   │   ├── __init__.py
│   │   │   ├── matcher.py
│   │   │   └── similarity.py
│   │   └── nocodb_client/
│   │       ├── __init__.py
│   │       ├── client.py
│   │       ├── tickets.py
│   │       └── comments.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── ticket.py
│   │   └── enrichment.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── config.py
│   └── main.py
├── tests/
│   ├── test_email_parser.py
│   ├── test_ai_enrichment.py
│   ├── test_ticket_matcher.py
│   └── test_nocodb_client.py
├── config/
│   ├── prompts/
│   │   ├── classification.txt
│   │   ├── extraction.txt
│   │   └── summary.txt
│   └── categories.json
├── scripts/
│   ├── setup_nocodb.py
│   ├── test_pipeline.py
│   └── migrate_db.py
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   └── deployment.md
├── .env.example
├── requirements.txt
├── setup.py
├── Dockerfile
└── README.md
```

## Configuration

### Variables d'Environnement

```env
# Email Configuration
EMAIL_PROVIDER=imap
IMAP_HOST=imap.example.com
IMAP_PORT=993
IMAP_USERNAME=tickets@example.com
IMAP_PASSWORD=secret

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# NocoDB Configuration
NOCODB_BASE_URL=https://nocodb.example.com
NOCODB_API_TOKEN=your-api-token
NOCODB_PROJECT_ID=your-project-id

# Application Configuration
LOG_LEVEL=INFO
PROCESSING_INTERVAL=60
MAX_EMAILS_PER_BATCH=10
```

## Installation

```bash
# Cloner le repository
git clone https://github.com/Devloupio/models.git
cd models/mail2tickets

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

# Installer dépendances
pip install -r requirements.txt

# Configurer variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# Initialiser base de données NocoDB
python scripts/setup_nocodb.py

# Lancer application
python src/main.py
```

## Utilisation

### Traitement Manuel d'un Email

```python
from src.services.email_parser import EmailParser
from src.services.ai_enrichment import AIEnricher
from src.services.ticket_matcher import TicketMatcher
from src.services.nocodb_client import NocoDBClient

# Parser l'email
parser = EmailParser()
parsed_email = parser.parse(raw_email)

# Enrichir avec IA
enricher = AIEnricher()
enriched = enricher.enrich(parsed_email)

# Matcher ou créer ticket
matcher = TicketMatcher()
ticket = matcher.match_or_create(enriched)

# Persister dans NocoDB
client = NocoDBClient()
client.save_ticket(ticket)
```

## Tests

```bash
# Tests unitaires
pytest tests/

# Tests d'intégration
pytest tests/integration/

# Coverage
pytest --cov=src tests/
```

## Roadmap

### MVP (Phase 1)
- [x] Architecture de base
- [ ] Service d'ingestion IMAP
- [ ] Parser email de base
- [ ] Intégration OpenAI (classification + extraction)
- [ ] Client NocoDB basique
- [ ] Matching simple (par Message-ID et sujet)
- [ ] Pipeline end-to-end fonctionnel

### Phase 2
- [ ] Support POP3 et SMTP Webhook
- [ ] Gestion avancée des threads
- [ ] Embeddings pour similarité de tickets
- [ ] Détection d'escalade
- [ ] Priorisation dynamique

### Phase 3
- [ ] Suggestion de réponses
- [ ] Base de connaissance et articles
- [ ] Apprentissage continu
- [ ] Tableau de bord et analytics
- [ ] API REST publique

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## License

MIT License - voir LICENSE file

## Support

Pour toute question ou support, contacter : support@devloupio.com
