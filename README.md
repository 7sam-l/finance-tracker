# Fintrack — Personal Finance Tracker

Stack: Python + Flask | React + Vite | SQLite + SQLAlchemy


## Manual Setup

# Backend setup

cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Database setup
flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade

# Seed initial data
python seed.py

# Run backend server
python run.py

### Frontend
cd frontend && npm install && npm run dev

### Tests
cd backend && pytest app/tests/ -v

## API
GET/POST /api/transactions/
DELETE   /api/transactions/:id
GET/POST /api/categories/
GET      /api/summary/

## Key Decisions
- Marshmallow schemas own all validation — clear single-responsibility boundary
- Transaction type must match category type — enforced in routes, tested explicitly
- App factory pattern — same code runs with different configs (prod/test)
- All errors flow through utils.py helpers — consistent shape, centralized logging
- All frontend API calls centralized in services/api.js
