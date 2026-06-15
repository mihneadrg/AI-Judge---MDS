@echo off
python -X utf8 -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
