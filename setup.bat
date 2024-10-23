set PYTHONPATH=%PYTHONPATH%;%cd%
python ./BattleFactoryBuddy/StaticDataGenerator.py
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py runserver
