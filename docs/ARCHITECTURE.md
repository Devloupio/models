# Architecture Mail2Tickets - Diagrammes

## Vue d'ensemble du système

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          MAIL2TICKETS SYSTEM                            │
│                  Intelligent Email-to-Ticket Conversion                 │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Email Sources   │
│                  │
│ • IMAP Server    │
│ • POP3 Server    │
│ • SMTP Webhook   │
└────────┬─────────┘
         │
         │ Raw Emails
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     SERVICE: Email Ingestion                           │
│  • Connect to email sources                                            │
│  • Fetch new messages                                                  │
│  • Mark as processed                                                   │
└────────┬───────────────────────────────────────────────────────────────┘
         │
         │ Raw Email Object
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     SERVICE: Email Parser                              │
│  • Extract headers (Message-ID, Subject, From, To, etc.)              │
│  • Parse multipart content                                            │
│  • Extract attachments                                                │
│  • Clean signatures and citations                                     │
│  • Detect thread (In-Reply-To, References)                           │
└────────┬───────────────────────────────────────────────────────────────┘
         │
         │ ParsedEmail
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     SERVICE: AI Enrichment (OpenAI)                    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Prompt: Classification                                       │    │
│  │ → Category (incident/request/change/problem)                │    │
│  │ → Subcategory                                               │    │
│  │ → Urgency, Impact → Priority                                │    │
│  │ → Summary, Keywords                                         │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Prompt: Entity Extraction                                    │    │
│  │ → Client/Organization                                        │    │
│  │ → Site/Location                                             │    │
│  │ → Configuration Items (CI)                                  │    │
│  │ → Contacts                                                  │    │
│  │ → References (ticket ID, order number, etc.)                │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Prompt: Summary Generation                                   │    │
│  │ → Concise 2-3 sentence summary                              │    │
│  │ → Who, What, Impact, Context                                │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
└────────┬───────────────────────────────────────────────────────────────┘
         │
         │ AIEnrichment
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     SERVICE: Ticket Matcher                            │
│                                                                        │
│  Decision Logic:                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ 1. Check detected_ticket_number from parsing                │    │
│  │ 2. Search by Message-ID in email_threads table              │    │
│  │ 3. Search by In-Reply-To in email_threads table             │    │
│  │ 4. Search by References in email_threads table              │    │
│  │ 5. Search by normalized subject                             │    │
│  │ 6. (Optional) Search by similarity using embeddings         │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  Result:                                                               │
│  • If found → Update existing ticket + add comment                    │
│  • If not found → Create new ticket                                   │
│                                                                        │
└────────┬───────────────────────────────────────────────────────────────┘
         │
         │ Ticket Decision
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     SERVICE: NocoDB Client                             │
│                                                                        │
│  Create New Ticket:                                                   │
│  • Generate ticket_number (TICKET-XXXX)                               │
│  • POST /api/v2/tables/tickets/records                                │
│  • POST /api/v2/tables/email_threads/records                          │
│  • POST /api/v2/tables/ticket_comments/records                        │
│                                                                        │
│  Update Existing Ticket:                                              │
│  • PATCH /api/v2/tables/tickets/records/{id}                          │
│  • POST /api/v2/tables/ticket_comments/records                        │
│  • POST /api/v2/tables/email_threads/records                          │
│                                                                        │
└────────┬───────────────────────────────────────────────────────────────┘
         │
         │ Success/Failure
         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          NocoDB / PostgreSQL                           │
│                                                                        │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐       │
│  │   tickets    │   comments   │   threads    │   clients    │       │
│  └──────────────┴──────────────┴──────────────┴──────────────┘       │
│  ┌──────────────┬──────────────┬──────────────┐                      │
│  │    sites     │      CI      │  categories  │                      │
│  └──────────────┴──────────────┴──────────────┘                      │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Flux de données détaillé

### Scénario 1 : Nouvel email → Nouveau ticket

```
Email IMAP
    ↓
[Ingestion] Fetch email
    ↓
[Parser] 
    • Extract: Message-ID: <abc123@example.com>
    • Subject: "Mon imprimante ne fonctionne pas"
    • From: user@company.com
    • Body: "Bonjour, l'imprimante HP-301 du 3e étage..."
    ↓
[AI Enrichment]
    • Classification:
        - Category: incident
        - Subcategory: hardware_failure
        - Priority: medium
        - Summary: "Imprimante HP-301 du 3e étage HS"
    • Extraction:
        - CI: "HP-301"
        - Site: "3e étage"
        - Client: "company.com" → lookup in DB
    ↓
[Ticket Matcher]
    • Search Message-ID: <abc123@example.com> → NOT FOUND
    • Decision: CREATE NEW TICKET
    ↓
[NocoDB Client]
    • Generate ticket_number: "TICKET-0001"
    • Create ticket record
    • Create email_thread record
    • Create initial comment
    ↓
[Database]
    • tickets: id=1, ticket_number=TICKET-0001, status=new
    • email_threads: ticket_id=1, message_id=<abc123@example.com>
    • ticket_comments: ticket_id=1, comment_text="Imprimante..."
```

### Scénario 2 : Réponse à un email → Update ticket existant

```
Email IMAP
    ↓
[Ingestion] Fetch reply email
    ↓
[Parser]
    • Extract: Message-ID: <xyz789@example.com>
    • Subject: "Re: [TICKET-0001] Mon imprimante ne fonctionne pas"
    • In-Reply-To: <abc123@example.com>
    • From: support@company.com
    • Body: "Nous avons redémarré l'imprimante..."
    ↓
[AI Enrichment]
    • Classification:
        - Category: incident
        - Related_ticket: "TICKET-0001" (from subject)
    • Summary: "Imprimante redémarrée par le support"
    ↓
[Ticket Matcher]
    • Detected ticket: "TICKET-0001" from subject
    • Search In-Reply-To: <abc123@example.com> → FOUND ticket_id=1
    • Decision: UPDATE EXISTING TICKET
    ↓
[NocoDB Client]
    • Update ticket: status=in_progress
    • Create new comment
    • Create email_thread record
    ↓
[Database]
    • tickets: id=1, status=in_progress, updated_at=now()
    • email_threads: ticket_id=1, message_id=<xyz789@example.com>
    • ticket_comments: id=2, ticket_id=1, comment_text="Nous avons..."
```

## Architecture des modèles de données

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA MODELS                             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Ticket                                                           │
├──────────────────────────────────────────────────────────────────┤
│ - id: int                                                        │
│ - ticket_number: str (TICKET-0001)                              │
│ - subject: str                                                   │
│ - description: str                                               │
│ - status: TicketStatus (new, assigned, in_progress, ...)        │
│ - priority: TicketPriority (low, medium, high, critical)        │
│ - category: str (incident, request, change, problem)            │
│ - urgency: UrgencyLevel                                         │
│ - impact: ImpactLevel                                           │
│ - requester_email: str                                          │
│ - client_id: int (FK → clients)                                 │
│ - site_id: int (FK → sites)                                     │
│ - ci_id: int (FK → configuration_items)                         │
│ - created_at, updated_at, resolved_at, closed_at: datetime      │
│                                                                  │
│ + to_dict() → Dict                                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ ParsedEmail                                                      │
├──────────────────────────────────────────────────────────────────┤
│ - message_id: str                                                │
│ - subject: str                                                   │
│ - from_address: EmailAddress                                     │
│ - to_addresses: List[EmailAddress]                              │
│ - in_reply_to: Optional[str]                                     │
│ - references: List[str]                                          │
│ - thread_id: Optional[str]                                       │
│ - text_content: str                                              │
│ - html_content: str                                              │
│ - cleaned_content: str                                           │
│ - attachments: List[EmailAttachment]                            │
│ - detected_ticket_number: Optional[str]                          │
│                                                                  │
│ + to_dict() → Dict                                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ AIEnrichment                                                     │
├──────────────────────────────────────────────────────────────────┤
│ - classification: AIClassification                               │
│   ├─ category: TicketCategory                                   │
│   ├─ subcategory: str                                           │
│   ├─ urgency, impact, priority                                  │
│   └─ summary, keywords                                          │
│                                                                  │
│ - entities: List[ExtractedEntity]                               │
│   ├─ entity_type: str                                           │
│   ├─ value: str                                                 │
│   └─ confidence: float                                          │
│                                                                  │
│ - client_name, site_name, ci_name: Optional[str]                │
│ - related_ticket_number: Optional[str]                           │
│ - is_follow_up: bool                                            │
│                                                                  │
│ + to_dict() → Dict                                              │
└──────────────────────────────────────────────────────────────────┘
```

## Schéma de base de données (Relations)

```
┌─────────────┐
│  categories │
│             │
│ id ────┐    │
│ name   │    │
│ parent_id ──┘ (self-referencing)
└─────────────┘

┌─────────────┐         ┌─────────────┐         ┌──────────────────┐
│   clients   │         │    sites    │         │ configuration_   │
│             │         │             │         │     items        │
│ id ─────────┼────────→│ client_id   │         │                  │
│ name        │         │ id ─────────┼────────→│ site_id          │
│ email_domain│         │ name        │         │ id               │
│ sla_level   │         │ address     │         │ name             │
└─────────────┘         │ city        │         │ type             │
                        └─────────────┘         │ status           │
                                                └──────────────────┘
                                                        │
        ┌───────────────────────────────────────────────┤
        │                                               │
        ▼                                               │
┌─────────────────────────────────────────────────────────────────┐
│                           tickets                               │
│                                                                 │
│ id ────┐                                                        │
│ ticket_number                                                   │
│ subject, description                                            │
│ status, priority, category                                      │
│ requester_email, requester_name                                 │
│ assigned_to                                                     │
│ client_id  ──────→ clients.id                                   │
│ site_id    ──────→ sites.id                                     │
│ ci_id      ──────→ configuration_items.id                       │
│ urgency, impact                                                 │
│ created_at, updated_at, resolved_at, closed_at                  │
└───────┬─────────────────────────────────────────────────────────┘
        │
        │                    ┌─────────────────────────────────────┐
        ├───────────────────→│      ticket_comments                │
        │                    │                                     │
        │                    │ id                                  │
        │                    │ ticket_id ──→ tickets.id            │
        │                    │ comment_text                        │
        │                    │ author_email, author_name           │
        │                    │ is_internal                         │
        │                    │ created_at                          │
        │                    └─────────────────────────────────────┘
        │
        │                    ┌─────────────────────────────────────┐
        └───────────────────→│      email_threads                  │
                             │                                     │
                             │ id                                  │
                             │ ticket_id ──→ tickets.id (nullable) │
                             │ message_id (unique)                 │
                             │ in_reply_to                         │
                             │ references (JSON)                   │
                             │ thread_id                           │
                             │ subject                             │
                             │ from_email                          │
                             │ to_emails (JSON)                    │
                             │ received_at, processed_at           │
                             └─────────────────────────────────────┘
```

## Configuration et déploiement

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONFIGURATION LAYERS                        │
└─────────────────────────────────────────────────────────────────┘

.env file
    ↓
Environment Variables
    ↓
src/utils/config.py (Config class)
    ↓
    ├─→ Email settings (IMAP/POP3/Webhook)
    ├─→ OpenAI settings (API key, model, tokens)
    ├─→ NocoDB settings (URL, token, project)
    ├─→ Application settings (log level, intervals)
    └─→ Feature flags (auto-categorize, mock modes)
    ↓
config.validate()
    ↓
    • Check required variables
    • Validate formats
    • Test connections (optional)
    ↓
Application startup
```

## Pipeline de traitement (Boucle principale)

```
┌─────────────────────────────────────────────────────────────────┐
│                      MAIN PROCESSING LOOP                       │
└─────────────────────────────────────────────────────────────────┘

START
  ↓
[Initialize]
  • Load config
  • Validate
  • Setup logging
  • Connect to services
  ↓
[Main Loop] Every PROCESSING_INTERVAL seconds
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Email Ingestion                                      │
  │    • Connect to email source                            │
  │    • Fetch MAX_EMAILS_PER_BATCH new emails              │
  │    • Return list of raw emails                          │
  └─────────────┬───────────────────────────────────────────┘
                ↓
  ┌─────────────────────────────────────────────────────────┐
  │ 2. For each email:                                      │
  │    ↓                                                     │
  │    [Parse Email]                                        │
  │    • Extract metadata                                   │
  │    • Clean content                                      │
  │    • Detect thread                                      │
  │    ↓                                                     │
  │    [AI Enrichment]                                      │
  │    • Classify                                           │
  │    • Extract entities                                   │
  │    • Summarize                                          │
  │    ↓                                                     │
  │    [Match Ticket]                                       │
  │    • Search existing                                    │
  │    • Decide create/update                               │
  │    ↓                                                     │
  │    [Persist to NocoDB]                                  │
  │    • Create/update ticket                               │
  │    • Add comment                                        │
  │    • Store thread                                       │
  │    ↓                                                     │
  │    [Log & Metrics]                                      │
  │    • Processing time                                    │
  │    • Success/failure                                    │
  │    • Errors if any                                      │
  └─────────────┬───────────────────────────────────────────┘
                ↓
  [Wait PROCESSING_INTERVAL]
  ↓
  [Loop back]
```

---

Cette architecture assure une séparation claire des responsabilités, une scalabilité horizontale possible (chaque service peut être indépendant), et une maintenance facilitée.
