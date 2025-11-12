# Project Setup Instructions

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git
- AWS/GCP/Azure account (for cloud deployment)
- API keys:
  - OpenAI API key
  - Greenhouse API credentials (for integration testing)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd MLCOMP
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm
```

4. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys and configuration
```

Example `.env` file:
```
# Application
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# OpenAI
OPENAI_API_KEY=sk-...

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=recruitment_ai
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password

MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=recruitment_ai

REDIS_HOST=localhost
REDIS_PORT=6379

# ATS Integration
GREENHOUSE_API_KEY=your-greenhouse-api-key
GREENHOUSE_WEBHOOK_SECRET=your-webhook-secret

LEVER_API_KEY=your-lever-api-key

# AWS (for production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET=recruitment-ai-resumes
```

5. **Start services with Docker Compose**
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- MongoDB (port 27017)
- Redis (port 6379)
- Kafka (port 9092)

6. **Run database migrations**
```bash
# PostgreSQL migrations
python scripts/db_migrate.py

# MongoDB setup
python scripts/setup_mongodb.py
```

7. **Start the application**
```bash
# Development server
uvicorn main:app --reload --port 8000
```

8. **Access the API**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_jd_optimization.py

# Run specific test
pytest tests/test_jd_optimization.py::test_generate_jd
```

### Project Structure

```
MLCOMP/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── docker-compose.yml               # Local development services
├── Dockerfile                       # Container image
├── README.md                        # Project overview
│
├── modules/                         # Core modules
│   ├── jd-optimization/
│   │   ├── README.md
│   │   ├── api.py                  # API endpoints
│   │   ├── generator.py            # JD generation logic
│   │   ├── nlp_analyzer.py         # NLP analysis
│   │   └── seo_optimizer.py        # SEO optimization
│   │
│   ├── candidate-scoring/
│   │   ├── README.md
│   │   ├── api.py
│   │   ├── parser.py               # Resume parsing
│   │   ├── matcher.py              # Semantic matching
│   │   └── explainability.py       # XAI layer
│   │
│   ├── skill-gap-analysis/
│   │   ├── README.md
│   │   ├── api.py
│   │   ├── taxonomy.py             # Skill taxonomy
│   │   └── recommendations.py      # Gap analysis
│   │
│   └── bias-fairness-analyzer/
│       ├── README.md
│       ├── api.py
│       ├── disparate_impact.py     # Disparate impact analysis
│       ├── proxy_detector.py       # Proxy detection
│       ├── debiasing.py            # Debiasing techniques
│       └── compliance.py           # Compliance reports
│
├── integrations/                    # ATS integrations
│   ├── greenhouse/
│   │   ├── client.py
│   │   └── webhook.py
│   ├── lever/
│   │   ├── client.py
│   │   └── webhook.py
│   └── universal/
│       └── webhook.py
│
├── core/                            # Core infrastructure
│   ├── auth.py                     # Authentication
│   ├── database.py                 # Database connections
│   ├── cache.py                    # Redis caching
│   ├── queue.py                    # Message queue
│   └── config.py                   # Configuration
│
├── models/                          # Data models
│   ├── job.py
│   ├── candidate.py
│   ├── user.py
│   └── schemas.py
│
├── services/                        # Business logic
│   ├── ml_pipeline.py
│   ├── model_manager.py
│   └── analytics.py
│
├── tests/                           # Test suite
│   ├── test_jd_optimization.py
│   ├── test_candidate_scoring.py
│   ├── test_bias_analyzer.py
│   └── fixtures/
│
├── scripts/                         # Utility scripts
│   ├── db_migrate.py
│   ├── setup_mongodb.py
│   └── seed_data.py
│
├── docs/                            # Documentation
│   ├── architecture/
│   │   └── system-design.md
│   ├── integration/
│   │   └── ats-integration-strategy.md
│   ├── business/
│   │   └── business-model.md
│   └── roadmap/
│       └── development-roadmap.md
│
└── kubernetes/                      # K8s deployment configs
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

### Development Workflow

1. **Create feature branch**
```bash
git checkout -b feature/jd-optimization
```

2. **Write code and tests**
```bash
# Edit files
# Write tests in tests/

# Run tests frequently
pytest tests/test_your_feature.py
```

3. **Format code**
```bash
# Auto-format with black
black .

# Check style
flake8 .

# Type checking
mypy .
```

4. **Commit and push**
```bash
git add .
git commit -m "feat: add JD optimization module"
git push origin feature/jd-optimization
```

5. **Create pull request**
- Open PR on GitHub
- Ensure CI passes
- Request review

### Deployment

#### Docker Build

```bash
# Build image
docker build -t recruitment-ai:latest .

# Run container
docker run -p 8000:8000 \
  --env-file .env \
  recruitment-ai:latest
```

#### Kubernetes Deployment

```bash
# Apply configurations
kubectl apply -f kubernetes/

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/recruitment-ai
```

#### Production Deployment Checklist

- [ ] Set `APP_ENV=production` in environment
- [ ] Use production database credentials
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure logging (ELK stack)
- [ ] Set up alerts (PagerDuty, Opsgenie)
- [ ] Enable API rate limiting
- [ ] Configure backup strategy
- [ ] Disaster recovery plan documented
- [ ] Security audit completed
- [ ] Load testing passed

### Monitoring & Debugging

#### View Application Logs

```bash
# Docker
docker logs -f recruitment-ai

# Kubernetes
kubectl logs -f deployment/recruitment-ai

# Local
tail -f logs/app.log
```

#### Check Metrics

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

#### Database Access

```bash
# PostgreSQL
docker exec -it postgres psql -U postgres -d recruitment_ai

# MongoDB
docker exec -it mongodb mongosh

# Redis
docker exec -it redis redis-cli
```

### Common Issues

**Issue**: spaCy model not found
```bash
# Solution
python -m spacy download en_core_web_lg
```

**Issue**: OpenAI API rate limit
```bash
# Solution: Implement exponential backoff in code
# Or upgrade OpenAI plan
```

**Issue**: PostgreSQL connection refused
```bash
# Solution: Check if PostgreSQL is running
docker ps | grep postgres

# Restart if needed
docker-compose restart postgres
```

**Issue**: Out of memory errors with large resumes
```bash
# Solution: Increase worker memory limit in Docker
# Edit docker-compose.yml:
#   deploy:
#     resources:
#       limits:
#         memory: 4G
```

### Getting Help

- **Documentation**: See `/docs` directory
- **API Reference**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Slack**: #recruitment-ai-dev

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit pull request

See `CONTRIBUTING.md` for detailed guidelines.

### License

[To be determined]

---

**Questions?** Contact the development team or create an issue on GitHub.
