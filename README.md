# Fintrack — Personal Finance Tracker

Stack: Python + Flask | React + Vite | SQLite + SQLAlchemy


## Manual Setup

## Backend setup

cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## Database setup
flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade

## Seed initial data
python seed.py

## Run backend server
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

## Key Technical Decisions

1. **App Factory Pattern**
   We use Flask’s app factory to allow multiple configurations
   (development, testing, production) without code duplication.
   This pattern enables easier test setup and deployment flexibility.

2. **Marshmallow for Validation**
   Validation logic lives in Marshmallow schemas to enforce clear
   separation of concerns. This keeps route functions focused
   on request/response flow while schema definitions handle data
   validation and transformations.

3. **Transaction–Category Type Enforcement**
   The backend enforces that a transaction’s type must match its
   category’s type. This rule ensures data integrity and simplifies
   reporting logic.

4. **Centralized Error Handling**
   All errors route through `utils.py` helpers which produce
   consistent response shapes and centralized error logging.

5. **Centralized Frontend API Layer**
   All frontend API calls are wrapped in `services/api.js` to
   ensure consistent base URLs, headers, and error handling
   across components.

6. **Testing Strategy**
   Tests live in `backend/app/tests` and focus on core service
   logic and major edge cases. CI integration planned for future.

7. **Database Migrations**
   We use Flask-Migrate to track and version schema changes,
   making schema updates safe and repeatable across environments.
