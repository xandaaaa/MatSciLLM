install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	npm install -g serve

run:
	cd frontend && npm run build && serve -s dist &
	cd backend && uvicorn app:app --reload