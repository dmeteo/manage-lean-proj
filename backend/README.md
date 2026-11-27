# Бэкенд управления lean-проектами

Каркас на FastAPI, Pydantic, SQLAlchemy и Alembic. Структура каталогов основана на
проекте `AIMarket`. Внешний префикс API — `/api`; каталог `app/api/v1` не добавляет
`/v1` к адресам запросов.

## Что готово

- В `app/models/` описана предварительная схема БД; первая миграция находится в `migrations/`.
- В `app/schemas/` находятся черновые DTO запросов и ответов.
- В `app/api/v1/routers/` объявлены 40 маршрутов из рабочего API-контракта.
- [openapi.json](openapi.json) генерируется из приложения. При запуске схема доступна по `/openapi.json`, интерфейс Swagger — по `/docs`.
- [schema.dbml](schema.dbml) генерируется из моделей БД; файл можно вставить в DBML-редактор для построения диаграммы.
- [schema.mmd](schema.mmd) содержит те же таблицы и связи в формате Mermaid ER.
- Работает только `GET /health`. Остальные маршруты возвращают `501`.

Авторизация, проверка прав, переходы статусов, хранение файлов и отчёты пока не
реализованы. Cookie `lean_session` в схеме указана предварительно; наличие сессии
и CSRF-токена обработчики сейчас не проверяют. Модель БД и DTO ещё требуют ревью.

## Запуск

Нужны Python 3.12+, PostgreSQL и `make`. Из корня репозитория в PowerShell:

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\Activate.ps1
make install
Copy-Item backend/.env.example backend/.env
# Укажите параметры своей PostgreSQL в backend/.env.
make alembic-upgrade
make run
```

Основные команды Makefile:

| Команда | Назначение |
|---|---|
| `make help` | Показать команды |
| `make run` | Запустить FastAPI с автоперезагрузкой |
| `make alembic-migrate m="описание"` | Создать миграцию по изменениям моделей |
| `make alembic-upgrade` | Применить миграции |
| `make alembic-downgrade` | Откатить одну миграцию |
| `make export_openapi` | Обновить `backend/openapi.json` |
| `make export_dbml` | Обновить диаграмму БД в `backend/schema.dbml` |
| `make export_mermaid` | Обновить Mermaid-диаграмму в `backend/schema.mmd` |
| `make check` | Проверить компиляцию Python и актуальность OpenAPI |

Не добавляйте в Git `.env`, дампы БД, загруженные файлы и данные заказчика.
