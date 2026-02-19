# AI Guidance — Fintrack

This project was built using AI tools (Claude / ChatGPT) as development assistants.
AI was constrained by explicit rules and all generated output was reviewed before inclusion.

The goal was to use AI for acceleration while preserving correctness, clarity,
and long-term maintainability.

---

## How AI Was Used

AI tools were used to:
- Draft initial Flask routes and React components
- Suggest schema and validation patterns
- Generate boilerplate and documentation
- Review code for edge cases and readability

AI was not allowed to introduce business rules or bypass validation layers.

---

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

---

## Validation Rules

| Field        | Rule                                      |
|-------------|-------------------------------------------|
| amount      | Must be > 0                               |
| date        | Must not be in the future                 |
| type        | Must be "income" or "expense"             |
| category_id | Must reference an existing category       |
| type match  | Transaction type must match category type |
| description | Required, 1–200 chars                     |

---

## Frontend Rules

- All API calls go through `src/services/api.js` only
- Always display errors returned from the API
- Do not duplicate backend validation logic on the client

---

## Verification of AI Output

All AI-generated code was:
- Reviewed line-by-line
- Tested via API calls and frontend interaction
- Adjusted to match project conventions

Several AI suggestions were simplified or rejected
when they introduced unnecessary abstractions or weakened validation.

---

## Known AI Failure Modes

During development, AI occasionally:
- Suggested bypassing schema validation
- Over-generalized domain logic
- Introduced logic into route handlers

These suggestions were intentionally rejected to preserve system integrity.

---

## Why This File Exists

This file documents:
- Constraints imposed on AI behavior
- How AI output was verified
- How system correctness was protected

AI accelerated development, but all architectural and correctness decisions
were made intentionally.
