.PHONY: backend frontend seed test

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

seed:
	cd backend && python -m scripts.seed_database

test:
	cd backend && pytest -q
