# Models Repository

This repository contains TensorFlow Lite models for wake word detection and the **Mail2Tickets** intelligent ticketing system.

## Contents

### 1. Wake Word Detection Models (TFLite)

The following wake word detection models are available:

- `dit_manu.tflite` - "dit manu" wake word model
- `eh_maanoo.tflite` - "eh maanoo" wake word model  
- `eh_maanoo3.tflite` - "eh maanoo" wake word model (variant 3)
- `eh_maanoo42.tflite` - "eh maanoo" wake word model (variant 42)
- `et_manu.tflite` - "et manu" wake word model

Each model comes with a corresponding JSON configuration file containing metadata and parameters.

### 2. Mail2Tickets System

**Mail2Tickets** is an innovative intelligent ticketing system that automatically converts emails into structured tickets using AI (OpenAI) and stores them in a NocoDB/PostgreSQL database.

#### Key Features

- 📧 **Email Ingestion**: IMAP/POP3/SMTP webhook support
- 🧹 **Smart Parsing**: Automatic cleaning of email content (signatures, citations)
- 🤖 **AI Classification**: Automatic categorization, prioritization using OpenAI
- 🎯 **Entity Extraction**: Automatic detection of clients, sites, CIs, etc.
- 🔗 **Thread Detection**: Smart linking of email replies to existing tickets
- 💾 **NocoDB Integration**: Complete CRUD via NocoDB REST API
- 📊 **PostgreSQL Backend**: Robust data persistence

#### Quick Start

```bash
# Navigate to Mail2Tickets documentation
cat MAIL2TICKETS_README.md

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Install dependencies
pip install -r requirements.txt

# Initialize database schema
python scripts/setup_nocodb.py

# Run tests
python tests/test_basic.py

# Start application
python src/main.py
```

#### Architecture

```
Email Sources → Ingestion → Parsing → AI Enrichment → Ticket Matching → NocoDB Storage
                                ↓
                          OpenAI GPT-4
                          (Classification,
                           Extraction,
                           Summarization)
```

#### Documentation

- [Mail2Tickets Full Documentation](MAIL2TICKETS_README.md)
- [Database Schema](docs/database_schema.json)
- [API Configuration](.env.example)

## Repository Structure

```
models/
├── wake-word-models/       # TFLite wake word detection models
│   ├── dit_manu.*
│   ├── eh_maanoo.*
│   └── et_manu.*
│
├── src/                    # Mail2Tickets source code
│   ├── services/          # Core services
│   ├── models/            # Data models
│   └── utils/             # Utilities
│
├── tests/                  # Test suite
├── scripts/               # Setup and maintenance scripts
├── config/                # Configuration files and prompts
├── docs/                  # Documentation
│
├── MAIL2TICKETS_README.md # Mail2Tickets documentation
├── requirements.txt       # Python dependencies
└── .env.example          # Environment configuration template
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License

## Support

For questions or support, please open an issue in this repository.
