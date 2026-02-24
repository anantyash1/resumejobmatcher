#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model (if fails, continue)
python -m spacy download en_core_web_sm || pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl || echo "spaCy model installation skipped"

# Download NLTK data
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"

# Initialize database
python -c "from app.database import init_db; init_db(); print('Database initialized')"

# Seed database on first deploy
python -c "
from app.database import SessionLocal
from app.models import Company
db = SessionLocal()
if db.query(Company).count() == 0:
    print('Seeding database...')
    from app.utils.helpers import seed_all
    seed_all()
    print('Seeding complete!')
else:
    print('Database already seeded')
db.close()
"

echo "Build complete!"