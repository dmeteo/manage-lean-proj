# API-контракт v0.1 — проект для согласования

Этот документ уточняет рабочее ТЗ, а не описывает готовый сервер. Правила ролей и переходов: [BACKEND_SPEC](BACKEND_SPEC.md). До фиксации согласованной версии программирование приложения не начинается. После согласования backend оформляет OpenAPI с полными схемами, required/nullable, enum, примерами и ответами ошибок; frontend проверяет соответствие MSW. Markdown остаётся пояснением к утверждённой схеме.

## Общие правила

Базовый путь /api; JSON camelCase, UTF-8. UUID в строке; даты календаря YYYY-MM-DD, timestamp RFC3339 в UTC с Z. Сравнение today — Asia/Yekaterinburg. Денежные значения и KPI — десятичные строки без разделителей тысяч; деньги до 2, KPI до 4 знаков. null означает отсутствие значения. ID, автор, время, status, externalStatus и version ответа задаёт сервер.

Строки trim: name/title 1–200, displayName 1–100, login 3–100 (латиница, цифры, точка, _ и -), description/goal/problem/comment/source до 4000, unit 1–30. Возврат требует comment 1–4000. Неизвестные поля и enum → 400; недопустимые ссылки/даты → 400; коллизия login, версия или переход → 409. PATCH меняет только переданные разрешённые поля; null допустим только для nullable, непереданное поле сохраняется. PATCH не меняет роли/статусы через посторонние DTO.

Все изменяемые существующие ресурсы используют expectedVersion целого числа ≥1 в теле; сервер атомарно сравнивает и увеличивает version. Для файла POST это поле формы. Создание дочернего ресурса не изменяет Project.version; загрузка и решения меняют Activity.version. При 409 клиент перечитывает ресурс и предлагает повтор, не перезаписывает автоматически. Для смены участников используется версия Project. Повтор команды с устаревшей версией не выполняется.

Публично доступен только auth/login и получение CSRF; остальные маршруты требуют сессии. JSON-тела POST/PATCH, включая login/logout, требуют X-CSRF-Token, выданный GET /auth/csrf и связанный с cookie. GET не меняет бизнес-состояние. Ответы 401 очищают клиентское состояние входа. 404 скрывает существование чужого объекта; 403 означает запрет действия над доступным объектом. У всех маршрутов проверяется принадлежность ресурса проекту.

## Авторизация

| Метод и путь | Запрос | Успех |
|---|---|---|
| GET /auth/csrf | без тела | 200 {csrfToken:string}, cookie предварительной сессии |
| POST /auth/login | LoginRequest | 200 UserDto; Set-Cookie сессии, прежняя сессия заменяется |
| GET /auth/me | — | 200 UserDto |
| POST /auth/logout | {} | 204, отзыв сессии |

LoginRequest: login:string, password:string (не пустой, до 256; не логировать).
Cookie HttpOnly/Secure/SameSite=Lax, 8 часов. Клиент отправляет credentials; cookie не хранится в localStorage. После login заново получить CSRF. Для demo пароль задаётся вне Git; политика создания паролей — минимум 12 символов, до 256, согласуется при ревью. Не раскрывать существование логина при ошибке входа. Ограничение частоты → 429 и Retry-After.

UserDto: id, displayName, login, role, enterpriseId:UUID|null, isActive, version. Role: admin | coordinator | manager | approver | employee. Справочники не возвращают login; UserSummary: id, displayName, role, enterpriseId. Пользователь предприятия имеет обязательный enterpriseId, РЦК — null.

## Маршруты

Обозначения: C — координатор; M — назначенный РП; A — назначенный согласующий; E — назначенный сотрудник своего предприятия; Ad — администратор. Read означает C/M/A/E в области доступа. Матрица BACKEND_SPEC приоритетна; отсутствие явного разрешения означает запрет.

| Метод и путь | DTO запроса | Ответ / право |
|---|---|---|
| GET /enterprises | параметры списка | Page<EnterpriseDto>; Ad/C все, остальные только доступные |
| POST /enterprises | {name} | 201 EnterpriseDto; Ad |
| PATCH /enterprises/{id} | {name?,expectedVersion} | 200 EnterpriseDto; Ad |
| GET /users | параметры списка, role?, enterpriseId? | Page<UserDto>; Ad |
| POST /users | UserCreate | 201 UserDto; Ad |
| PATCH /users/{id} | UserUpdate | 200 UserDto; Ad |
| GET /projects/assignees | enterpriseId:UUID | Page<UserSummary>; C, только активные employee выбранного предприятия |
| GET /projects/managers | параметры списка | Page<UserSummary>; C, активные manager |
| GET /projects/approvers | параметры списка | Page<UserSummary>; C, активные approver |
| GET /projects | фильтры списка | Page<ProjectDto>; Read |
| POST /projects | ProjectCreate | 201 ProjectDto; C |
| GET /projects/{id} | — | 200 ProjectDto; Read |
| PATCH /projects/{id} | ProjectUpdate | 200 ProjectDto; M |
| PUT /projects/{id}/assignments | ProjectAssignments | 200 ProjectDto; C, draft/active |
| GET /projects/{id}/members | параметры списка | Page<UserSummary>; Read |
| POST /projects/{id}/status | ProjectTransition | 200 ProjectDto; M activate/complete, C archive |
| GET /projects/{id}/activities | фильтры списка | Page<ActivityDto>; Read |
| POST /projects/{id}/activities | ActivityCreate | 201 ActivityDto; M, active |
| GET /activities/{id} | — | 200 ActivityDto; Read |
| PATCH /activities/{id} | ActivityUpdate | 200 ActivityDto; M/E, поля по правилам |
| POST /activities/{id}/transitions | ActivityTransition | 200 ActivityDto; E |
| POST /activities/{id}/review | ReviewRequest | 200 ActivityDto; M/A по стадии |
| GET /activities/{id}/reviews | параметры списка | Page<ReviewDto>; Read |
| POST /activities/{id}/external-status | ExternalStatusRequest | 200 ActivityDto; C |
| GET /activities/{id}/files | параметры списка | Page<DocumentDto>; Read |
| POST /activities/{id}/files | multipart, ниже | 201 DocumentDto; M/E |
| GET /files/{id}/download | — | 200 binary; Read |
| GET /projects/{id}/metrics | параметры списка | Page<MetricDto>; Read |
| POST /projects/{id}/metrics | MetricCreate | 201 MetricDto; M |
| PATCH /metrics/{id} | MetricUpdate | 200 MetricDto; M |
| GET /projects/{id}/effects | параметры списка | Page<EffectDto>; Read |
| POST /projects/{id}/effects | EffectCreate | 201 EffectDto; M |
| PATCH /effects/{id} | EffectUpdate | 200 EffectDto; M |
| GET /dashboard | enterpriseId? | 200 DashboardDto; Read, только доступная область |
| GET /projects/{id}/export | format=csv | 200 text/csv; Read |
| GET /audit | entityType?, entityId?, параметры списка | Page<AuditDto>; Ad/C |

PUT assignments заменяет весь набор назначений, а не дополняет его. Удалять участника с назначенным незавершённым мероприятием нельзя → 409; сначала переназначить мероприятие. Деактивация пользователя с активными назначениями также →409. DELETE, восстановление архива, сброс пароля и самостоятельная регистрация не входят в API первой итерации. Ad не получает доступ к бизнес-файлам через администрирование.

201 включает Location конкретного ресурса; для files — /api/files/{id}/download. GET-списки пусты как 200 с items=[], карточка отсутствующего объекта —404.

## DTO

Ниже типы: string, UUID, date, timestamp, int, bool, decimalString; ? в запросе означает необязательное поле, nullable указан отдельно. DTO ответа перечисляют поля полностью; ссылки возвращаются ID, подписи получаются через name/displayName указанных справочников или поля summary.

- EnterpriseDto: id, name, version.
- UserCreate: displayName, login, password, role, enterpriseId:UUID|null. UserUpdate: displayName?, role?, enterpriseId?:UUID|null, isActive?, expectedVersion. Пароль PATCH не принимает.
- ProjectCreate: name, enterpriseId, managerId, approverId, memberIds:UUID[], startDate, plannedEndDate, goal?:string|null, problem?:string|null, description?:string|null. Сервер создаёт draft, actualEndDate=null.
- ProjectUpdate: name?, startDate?, plannedEndDate?, goal?:string|null, problem?:string|null, description?:string|null, expectedVersion. Предприятие неизменно после создания.
- ProjectAssignments: managerId, approverId, memberIds:UUID[], expectedVersion.
- ProjectTransition: action:activate|complete|archive, actualEndDate?:date, expectedVersion. complete требует дату; запрещён до решения D4.
- ProjectDto: id, name, enterpriseId, enterpriseName, managerId, managerName, approverId, approverName, startDate, plannedEndDate, actualEndDate:date|null, goal/problem/description:string|null, status, archivedFromStatus:string|null, progressPercent:int, version, createdAt, updatedAt.
- ActivityCreate: title, assigneeId, plannedEndDate, plannedStartDate?:date|null, stage?:string|null, isRequired?:bool (default true), requiresDocument?:bool (default true), sortOrder?:int (default 0, ≥0). Создаётся planned, actualEndDate=null, externalStatus=notSent.
- ActivityUpdate: title?, stage?:string|null, assigneeId?, plannedStartDate?:date|null, plannedEndDate?, isRequired?, requiresDocument?, sortOrder?, actualEndDate?:date|null, comment?:string|null, expectedVersion. M меняет только поля плана/назначения, E только actualEndDate/comment своего задания; поля вне роли →403.
- ActivityTransition: action:start|submit, expectedVersion. start: planned/returned →inProgress; submit: inProgress →managerReview.
- ActivityDto: id, projectId, title, stage:string|null, assigneeId, assigneeName, plannedStartDate:date|null, plannedEndDate, actualEndDate:date|null, comment:string|null, isRequired, requiresDocument, sortOrder, status, externalStatus, externalRecordedAt:timestamp|null, externalRecordedBy:UUID|null, externalComment:string|null, isOverdue:bool, completedLate:bool, reviewCycle:int (0 до первой отправки), version, createdAt, updatedAt.
- ReviewRequest: decision:approve|return, comment?:string|null, expectedVersion. return требует непустой comment. Стадия определяется сервером: M managerReview→approverReview, A approverReview→internallyApproved.
- ReviewDto: id, activityId, cycle, stage:manager|approver, actorId, decision:approve|return, comment:string|null, createdAt.
- ExternalStatusRequest: status:sent|accepted|returned, comment?:string|null, expectedVersion. returned требует причину. Время и автор от сервера; ответ не является ответом портала.
- DocumentDto: id, activityId, originalName, mediaType, sizeBytes:int, uploadedBy, uploadedAt, kind:report|calculation|confirmation|other, revision:int, activityVersion:int. storageKey и путь никогда не возвращаются.
- MetricCreate: name, unit, plan:decimalString|null, actual:decimalString|null, recordedDate:date, source?:string|null. Хотя бы одно из plan/actual не null.
- MetricUpdate: name?, unit?, plan?:decimalString|null, actual?:decimalString|null, recordedDate?, source?:string|null, expectedVersion.
- MetricDto: id, projectId, name, unit, plan:decimalString|null, actual:decimalString|null, recordedDate, source:string|null, version.
- EffectCreate: type:actual|potential|releasedFunds, amount:decimalString, currency:RUB, periodStart:date, periodEnd:date, calculationDocumentId?:UUID|null, confirmationDocumentId?:UUID|null.
- EffectUpdate: поля EffectCreate необязательны + expectedVersion; type/currency могут передаваться только допустимыми enum.
- EffectDto: id, projectId, type, amount, currency, periodStart, periodEnd, calculationDocumentId:UUID|null, confirmationDocumentId:UUID|null, version.
- DashboardDto: activeProjects:int, inProgressActivities:int, overdueActivities:int, pendingReviews:int, upcomingActivities:ActivityDto[] (до 10, срок по возрастанию затем id), asOf:timestamp.
- AuditDto: id, actorId, entityType:project|activity|document|review|metric|effect|user|enterprise, entityId, action:string, timestamp, changeSummary:string. Не содержит секретов; C получает только бизнес-события доступных проектов, Ad — метаданные всех событий.

Metric/Effect редактируются только в active проекте. Предел decimal: 18 значащих цифр; periodEnd≥periodStart. Назначения валидируются по модели BACKEND_SPEC. Пустые обязательные строки, повтор memberIds, отрицательная version/size, неверные ссылки отклоняются. Даты мероприятия внутри периода проекта; сужение дат проекта при выходящих за них мероприятиях →409. Нельзя менять план у completed/archived.

## Статусы

Project.status: draft | active | completed | archived.

Activity.status: planned | inProgress | managerReview | approverReview | returned | internallyApproved.

Activity.externalStatus: notSent | sent | accepted | returned.

Это согласуемые уточнения ТЗ. Сервер возвращает эти значения, UI переводит подписи на русский. Не использовать одно returned без указания поля. Переходы полностью описаны в BACKEND_SPEC; PATCH не обходит проверки. При внешнем возврате сохраняется externalStatus=returned, Activity.status=returned. accepted и internallyApproved имеют разный смысл.

## Списки, поиск, сортировка

Все табличные GET поддерживают page (с 1, default 1), pageSize (default 20, 1–100), sort и direction=asc|desc (default asc). Стабильная дополнительная сортировка по id; total после ограничения прав/фильтров. Неизвестные параметры/поля сортировки →400.

| Список | Фильтры | sort (default) |
|---|---|---|
| projects | search по name без учёта регистра; enterpriseId, managerId, status | name, plannedEndDate, status (name) |
| activities | search по title; assigneeId, status, externalStatus, isOverdue | sortOrder, plannedEndDate, status (sortOrder) |
| enterprises/users | search по name/displayName; у users role, enterpriseId, isActive | name / displayName (то же) |
| assignees/managers/approvers/members | search по displayName; assignees требует enterpriseId | displayName |
| files | kind | uploadedAt (asc) |
| reviews | stage | createdAt (asc) |
| metrics | search по name | name, recordedDate (name) |
| effects | type | periodStart (asc) |
| audit | entityType, entityId | timestamp (asc) |

Dashboard enterpriseId ограничивается доступной областью; не расширяет права. CSV только выбранный проект целиком, без параметров пагинации. Невалидный UUID/дата/булево →400.

Page<T>:
```json
{"items":[],"page":1,"pageSize":20,"total":0}
```

## Примеры JSON

Создание проекта координатором, POST /api/projects:
```json
{
  "name":"Демонстрационный поток",
  "enterpriseId":"10000000-0000-4000-8000-000000000001",
  "managerId":"20000000-0000-4000-8000-000000000001",
  "approverId":"20000000-0000-4000-8000-000000000002",
  "memberIds":["20000000-0000-4000-8000-000000000003"],
  "startDate":"2026-11-26",
  "plannedEndDate":"2026-12-20"
}
```

201:
```json
{
  "id":"30000000-0000-4000-8000-000000000001",
  "name":"Демонстрационный поток",
  "enterpriseId":"10000000-0000-4000-8000-000000000001",
  "enterpriseName":"Демо-предприятие А",
  "managerId":"20000000-0000-4000-8000-000000000001",
  "managerName":"Демо РП",
  "approverId":"20000000-0000-4000-8000-000000000002",
  "approverName":"Демо согласующий",
  "startDate":"2026-11-26",
  "plannedEndDate":"2026-12-20",
  "actualEndDate":null,
  "goal":null,
  "problem":null,
  "description":null,
  "status":"draft",
  "archivedFromStatus":null,
  "progressPercent":0,
  "version":1,
  "createdAt":"2026-11-26T09:00:00Z",
  "updatedAt":"2026-11-26T09:00:00Z"
}
```

PATCH /api/activities/40000000-0000-4000-8000-000000000001 исполнителем:
```json
{"actualEndDate":"2026-11-27","comment":"Демонстрационный отчёт готов","expectedVersion":2}
```

POST /api/activities/40000000-0000-4000-8000-000000000001/review согласующим на approverReview:
```json
{"decision":"return","comment":"Уточнить исходные данные","expectedVersion":5}
```

Успешный PATCH/команда возвращает полный ActivityDto с увеличенной version, не частичный объект:
```json
{
  "id":"40000000-0000-4000-8000-000000000001",
  "projectId":"30000000-0000-4000-8000-000000000001",
  "title":"Подготовить отчёт",
  "stage":null,
  "assigneeId":"20000000-0000-4000-8000-000000000003",
  "assigneeName":"Демо исполнитель",
  "plannedStartDate":null,
  "plannedEndDate":"2026-11-27",
  "actualEndDate":"2026-11-27",
  "comment":"Демонстрационный отчёт готов",
  "isRequired":true,
  "requiresDocument":true,
  "sortOrder":0,
  "status":"returned",
  "externalStatus":"notSent",
  "externalRecordedAt":null,
  "externalRecordedBy":null,
  "externalComment":null,
  "isOverdue":false,
  "completedLate":false,
  "reviewCycle":1,
  "version":6,
  "createdAt":"2026-11-26T09:30:00Z",
  "updatedAt":"2026-11-27T10:00:00Z"
}
```

Причина возврата доступна в GET reviews (decision=return, comment), поле Activity.comment остаётся комментарием исполнителя.

POST metrics:
```json
{"name":"Время цикла","unit":"мин","plan":"10.0000","actual":"11.5000","recordedDate":"2026-11-27","source":"Демонстрационные измерения"}
```
201 MetricDto:
```json
{"id":"50000000-0000-4000-8000-000000000001","projectId":"30000000-0000-4000-8000-000000000001","name":"Время цикла","unit":"мин","plan":"10.0000","actual":"11.5000","recordedDate":"2026-11-27","source":"Демонстрационные измерения","version":1}
```

## Файлы

POST /activities/{id}/files: multipart/form-data, поля file (ровно один), kind (enum), expectedVersion (int). Лимит 20 МиБ на содержимое; общий HTTP-лимит должен учитывать multipart-обвязку. Сервер проверяет PDF/DOCX/XLSX/PNG/JPEG, размер, сигнатуру/структуру и права. Не принимает storageKey, автора или путь. Upload 201 DocumentDto, включая новую activityVersion. Повторная загрузка создаёт новый документ, revision = предыдущий максимум для activityId+kind +1; ревизия назначается атомарно. К загрузке применяются ограничения стадии из BACKEND_SPEC.

GET /files/{id}/download повторно проверяет права. Content-Type фактического допустимого типа, Content-Disposition: attachment, безопасное имя, X-Content-Type-Options: nosniff. Бинарные файлы не оборачиваются в JSON; ссылка на storage не выдаётся. 413 при превышении размера, 415 при неподдерживаемом типе, 400 при повреждённом контейнере. Не публиковать оригиналы заказчика в MSW fixtures.

## Ошибки

Content-Type application/problem+json. Единый ответ:
```json
{
  "type":"about:blank",
  "title":"Ошибка проверки данных",
  "status":400,
  "code":"validation_failed",
  "detail":"Проверьте заполнение полей.",
  "traceId":"demo-trace-001",
  "errors":{"plannedEndDate":["Дата окончания раньше даты начала."]}
}
```

errors — словарь массивов сообщений, пустой {} при ошибке без поля; остальные поля обязательны. Нет stack trace, SQL, внутренних путей и секретов.

| HTTP | code | Смысл |
|---|---|---|
| 400 | validation_failed | DTO/ссылки/даты невалидны |
| 401 | unauthenticated | нет действующей сессии/неверный вход |
| 403 | forbidden / csrf_invalid | запрещённое действие/CSRF |
| 404 | not_found | отсутствует или скрыт объект |
| 409 | version_conflict / invalid_transition / assignment_conflict / duplicate_login | конфликт без изменения данных |
| 413 | file_too_large | лимит файла |
| 415 | unsupported_media_type | тип запроса/файла |
| 429 | rate_limited | превышена частота |
| 500 | internal_error | непредвиденная ошибка, подробности только в закрытом журнале |

## MSW и интеграция

После согласования frontend реализует MSW по тем же путям, DTO, enum и правилам; идентификаторы примеров синтетические и стабильные. Общие fixtures: 2 предприятия, 2 проекта, ≥6 мероприятий, все роли, просрочка, возврат, пустая выдача. Mock должен изменять состояние в памяти, учитывать роли/версию и выдавать 400/401/403/404/409/413/415; успешный ответ на любой запрос не считается эмуляцией контракта. Отдельно эмулируются login/logout/me/CSRF и скачивание.

Чек-лист совместимости: обязательные поля и nullable; коды/формат ошибок; даты/decimal; порядок/total; два review-этапа; возврат; блокировка чужого файла; конфликт версии; одинаковые сводка/CSV. После подключения backend сценарии повторяются с MSW выключенным. В PR фиксируется версия/SHA контракта и реальные результаты; сейчас MSW и OpenAPI ещё не созданы.
