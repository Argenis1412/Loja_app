#! powershell
# Crear y activar entorno virtual, instalar deps y arrancar Uvicorn
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.api.main:app --reload
