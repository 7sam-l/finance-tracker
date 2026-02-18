# AI Guidance — Fintrack

## Core Constraints

### Never Do
- Bypass schema validation — all inputs must pass through Marshmallow schemas
- Allow transaction type to differ from its category type
- Write raw SQL — use SQLAlchemy ORM only
- Expose stack traces in API responses — use utils.py error helpers
- Skip db.session.commit() after mutations

### Always Do
- Run pytest after any backend change
- Use error_response / not_found / bad_request helpers for all errors
- Keep route handlers thin — no business logic in routes
- Log create/delete operations with logger.info()

## Validation Rules
| Field        | Rule                                          |
|-------------|-----------------------------------------------|
| amount      | Must be > 0                                   |
| date        | Must not be in the future                     |
| type        | Must be "income" or "expense"                 |
| category_id | Must reference an existing category           |
| type match  | Transaction type must match category type     |
| description | Required, 1–200 chars                         |

## Frontend Rules
- All API calls go through src/services/api.js only
- Always display errors returned from the API
