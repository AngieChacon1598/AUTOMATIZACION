#!/usr/bin/env python3
"""
Script de configuracion automatica para el Sistema de Seguimiento de Egresados
Ejecutar despues de clonar el proyecto
"""

import os
import sys
import subprocess
import shutil

def print_step(step, message):
    print(f"\n{'='*50}")
    print(f"PASO {step}: {message}")
    print(f"{'='*50}")

def run_command(command, description):
    print(f"\n[EJECUTANDO] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error en {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_file_exists(filepath, description):
    if os.path.exists(filepath):
        print(f"[OK] {description} - Existe")
        return True
    else:
        print(f"[ERROR] {description} - No encontrado")
        return False

def main():
    print("CONFIGURACION AUTOMATICA DEL PROYECTO")
    print("Sistema de Seguimiento de Egresados")
    
    # Paso 1: Verificar archivos necesarios
    print_step(1, "VERIFICANDO ARCHIVOS NECESARIOS")
    
    required_files = [
        ("requirements.txt", "Archivo de dependencias"),
        ("env.example", "Plantilla de configuracion"),
        ("run.py", "Punto de entrada de la aplicacion"),
        ("app/__init__.py", "Configuracion Flask")
    ]
    
    all_files_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n[ERROR] Faltan archivos necesarios. Verifica que hayas clonado el proyecto completo.")
        return False
    
    # Paso 2: Crear entorno virtual
    print_step(2, "CREANDO ENTORNO VIRTUAL")
    
    if os.path.exists("SegEgresados"):
        print("[OK] Entorno virtual ya existe")
    else:
        if not run_command("python -m venv SegEgresados", "Creando entorno virtual"):
            return False
    
    # Paso 3: Instalar dependencias
    print_step(3, "INSTALANDO DEPENDENCIAS")
    
    # Comando para Windows
    if sys.platform == "win32":
        pip_cmd = "SegEgresados\\Scripts\\pip"
    else:
        pip_cmd = "SegEgresados/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias"):
        return False
    
    # Paso 4: Crear archivo de configuracion
    print_step(4, "CONFIGURANDO VARIABLES DE ENTORNO")
    
    if os.path.exists("config.env"):
        print("[OK] Archivo config.env ya existe")
    else:
        if os.path.exists("env.example"):
            shutil.copy("env.example", "config.env")
            print("[OK] Archivo config.env creado desde env.example")
            print("[IMPORTANTE] Edita config.env con tus valores reales")
        else:
            print("[ERROR] No se encontro env.example")
            return False
    
    # Paso 5: Verificar configuracion
    print_step(5, "VERIFICANDO CONFIGURACION")
    
    # Verificar que se puede importar la aplicacion
    if sys.platform == "win32":
        python_cmd = "SegEgresados\\Scripts\\python"
    else:
        python_cmd = "SegEgresados/bin/python"
    
    test_import = f'{python_cmd} -c "from app import app; print(\'[OK] Aplicacion importada correctamente\')"'
    if not run_command(test_import, "Verificando importacion de la aplicacion"):
        print("[ADVERTENCIA] La aplicacion no se puede importar. Verifica config.env")
    
    # Paso 6: Instrucciones finales
    print_step(6, "CONFIGURACION COMPLETADA")
    
    print("""
CONFIGURACION COMPLETADA!

PROXIMOS PASOS:

1. Edita config.env con tus valores reales:
   - DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
   - JWT_SECRET_KEY (cambia por una clave segura)

2. Ejecuta la aplicacion:
   # Windows (PowerShell)
   SegEgresados\\Scripts\\Activate.ps1
   python run.py
   
   # Windows (CMD)
   SegEgresados\\Scripts\\activate.bat
   python run.py
   
   # Linux/Mac
   source SegEgresados/bin/activate
   python run.py

3. La aplicacion estara disponible en:
   http://localhost:5001

4. Login por defecto:
   Usuario: admin
   Contrasena: admin123

Si tienes problemas:
- Verifica que config.env este configurado correctamente
- Asegurate de que la base de datos este accesible
- Revisa los logs de la aplicacion

Listo para desarrollar!
    """)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n[OK] Configuracion completada exitosamente")
            sys.exit(0)
        else:
            print("\n[ERROR] Configuracion fallo")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[ADVERTENCIA] Configuracion cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        sys.exit(1)