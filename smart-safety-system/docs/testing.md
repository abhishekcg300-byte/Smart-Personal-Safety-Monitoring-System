# Testing

Run backend tests:
```
cd backend
pip install -r requirements.txt
pytest -q
```

Run backend:
```
uvicorn app.main:app --reload
```

Run web dashboard:
```
cd web-dashboard
npm install
npm run dev
```
API docs: http://127.0.0.1:8000/docs
