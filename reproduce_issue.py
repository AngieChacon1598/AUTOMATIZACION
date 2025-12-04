from app import app
from app.services.encuesta_egresado_service import obtener_encuestas
import sys

# Add current directory to path
sys.path.append('.')

with app.app_context():
    try:
        print("Testing pagination...")
        result = obtener_encuestas({}, page=1, per_page=10)
        print("Success!")
        print(result)
    except Exception as e:
        print("Error:")
        print(e)
        import traceback
        traceback.print_exc()
