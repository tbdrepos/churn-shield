.PHONY: dev build run clean

dev:
	cd frontend && npm install
	cd frontend && npm run dev
	cd backend && uvicorn app.main:app --reload

build:
	./scripts/build_frontend.sh

run:
	cd backend && uvicorn app.main:app

clean:
	rm -rf frontend/dist
