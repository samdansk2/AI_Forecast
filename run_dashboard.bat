@echo off
cd /d "C:\Users\Sk Samdan\Desktop\ML_project"
call .venv\Scripts\activate.bat
echo Starting AI Market Intelligence Dashboard...
streamlit run dashboard/enhanced_app.py
pause
