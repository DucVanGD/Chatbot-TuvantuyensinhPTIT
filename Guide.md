Chạy action server: 
'''
.\venv\Scripts\Activate.ps1
python -m rasa run actions
'''
Chạy server Rasa:
'''
.\venv\Scripts\Activate.ps1
python -m rasa run --enable-api --cors "*" --port 5005 --host 0.0.0.0 --model models
'''
Chạy server UI:
'''
.\venv\Scripts\Activate.ps1
python -m http.server 8000
'''
Link:
http://localhost:8000
http://<IP máy>:8000