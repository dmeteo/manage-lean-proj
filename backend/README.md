## Запуск

Нужны Python 3.12+, PostgreSQL и `make`. Из корня репозитория в PowerShell:

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
make install
make alembic-upgrade
make run
```
