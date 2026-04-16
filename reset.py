import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_SQLITE = BASE_DIR / "db.sqlite3"


# Activar el entorno virtual
VENV_ACTIVATE = BASE_DIR / ".venv" / "Scripts" / "Activate.ps1"
if VENV_ACTIVATE.exists():
    subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(VENV_ACTIVATE)],
        check=True,
    )
else:
    print(
        "No se encontró el script de activación del entorno virtual. Asegúrate de que el entorno esté configurado correctamente."
    )


def delete_migrations():
    print("Eliminando migraciones...")
    for app in BASE_DIR.iterdir():
        migrations = app / "migrations"
        if migrations.exists() and migrations.is_dir():
            for file in migrations.iterdir():
                if file.name != "__init__.py":
                    if file.is_file():
                        file.unlink()
                    else:
                        shutil.rmtree(file)
            print(f"  ✔ {app.name}")


def delete_database():
    if DB_SQLITE.exists():
        DB_SQLITE.unlink()
        print("Base de datos eliminada.")
    else:
        print("No se encontró base de datos.")


def recreate_database():
    print("Creando nuevas migraciones...")
    subprocess.run(["python", "manage.py", "makemigrations"], check=True)

    print("Aplicando migraciones...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)


def create_superuser():
    print("Creando superusuario...")

    script = """
from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
password = "1234"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superusuario creado: admin / 1234")
else:
    print("El superusuario ya existe.")
"""

    subprocess.run(
        ["python", "manage.py", "shell"],
        input=script,
        text=True,
        check=True,
    )


if __name__ == "__main__":
    print("RESET COMPLETO DE DJANGO")
    delete_migrations()
    delete_database()
    recreate_database()
    create_superuser()
    print("Proceso finalizado correctamente.")