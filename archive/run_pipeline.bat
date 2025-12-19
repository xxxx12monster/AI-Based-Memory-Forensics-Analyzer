@echo off
echo Running Data Preprocessing (Binary + Multiclass)...
python src/data_preprocessing.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Running Search Algorithm (Feature Selection)...
python src/search_algo.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Training Base Models...
python src/base_models.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Training Advanced Models (MLP, Ensemble, Anomaly Detection)...

python src/advanced_models.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo Starting Premium Dashboard...
streamlit run src/app.py
