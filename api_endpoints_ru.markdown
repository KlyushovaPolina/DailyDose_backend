# API-эндпоинты для фронтенда

Этот документ содержит список всех необходимых API-эндпоинтов для фронтенда приложения DailyDose. Эндпоинты сгруппированы по соответствующим файлам хранилищ (`auth-store.ts`, `medication-store.ts`, `settings-store.ts`). Все эндпоинты начинаются с базового URL `http://127.0.0.1:8000` или `http://147.45.185.112:8000` если запущено на сервере.

## Аутентификация (`auth-store.ts`)

### Регистрация нового пользователя
- **Метод**: `POST`
- **Путь**: `/api/auth/users/`
- **Тело запроса (JSON)**:
  ```json
  {
      "id": "123456",
      "name": "newuser",
      "email": "newuser@example.com",
      "password": "newpass123",
      "photoUrl": "url"
  }
  ```
- **Ожидаемый ответ (201 Создано)**:
  ```json
  {
      "id": "123456",
      "name": "newuser",
      "email": "newuser@example.com",
      "photoUrl": "url"
  }
  ```

### Вход (получение токена)
- **Метод**: `POST`
- **Путь**: `/api/auth/token/login/`
- **Описание**: Аутентифицирует пользователя и возвращает токен.
- **Тело запроса (JSON)**:
  ```json
  {
      "email": "newuser@example.com",
      "password": "newpass123"
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "auth_token": "your_token_here"
  }
  ```

### Выход (удаление токена)
- **Метод**: `POST`
- **Путь**: `/api/auth/token/logout/`
- **Описание**: Удаляет токен текущего пользователя (требуется аутентификация).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)

### Получение данных текущего пользователя
- **Метод**: `GET`
- **Путь**: `/api/auth/users/me/`
- **Описание**: Возвращает данные текущего авторизованного пользователя.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "some_string_id",
      "name": "newuser",
      "email": "newuser@example.com",
      "photoUrl": "url"
  }
  ```

### Обновление данных текущего пользователя
- **Метод**: `PATCH`
- **Путь**: `/api/auth/users/me/`
- **Описание**: Обновляет данные текущего пользователя (например, `name` или `email`).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "name": "updateduser",
      "email": "updateduser@example.com"
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "some_string_id",
      "name": "updateduser",
      "email": "updateduser@example.com",
      "photoUrl": "url"
  }
  ```

### Изменение пароля
- **Метод**: `POST`
- **Путь**: `/api/auth/users/set_password/`
- **Описание**: Позволяет авторизованному пользователю изменить свой пароль. Требуется токен.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "current_password": "oldpass123",
      "new_password": "newpass456"
  }
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)


## Управление медикаментами (`medication-store.ts`)

Для каждой из моделей далее реализованы все CRUD операции.

### Получение списка медикаментов
- **Метод**: `GET`
- **Путь**: `/api/medications/`
- **Описание**: Возвращает список медикаментов текущего пользователя (требуется аутентификация).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  [
      {
          "id": "1622548800001",
          "name": "Аспирин",
          "form": "tablet",
          "dosagePerUnit": "500mg",
          "unit": "mg",
          "instructions": "Принимать с едой",
          "totalQuantity": 30,
          "remainingQuantity": 25,
          "lowStockThreshold": 5,
          "trackStock": true,
          "iconName": "pill",
          "iconColor": "#FF0000",
          "createdAt": 1622548800000,
          "updatedAt": 1622548800000
      }
  ]
  ```

Так же есть возможность получить медикамент по Id

### Создание медикамента
- **Метод**: `POST`
- **Путь**: `/api/medications/`
- **Описание**: Создаёт новый медикамент для текущего пользователя.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "id": "1622548800002",
      "name": "Ибупрофен",
      "form": "tablet",
      "unit": "mg",
      "instructions": "Принимать с едой",
      "totalQuantity": 20,
      "remainingQuantity": 20,
      "lowStockThreshold": 5,
      "trackStock": true,
      "iconName": "pill",
      "iconColor": "#FF0000",
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```
- **Ожидаемый ответ (201 Создано)**:
  ```json
  {
      "id": "1622548800002",
      "name": "Ибупрофен",
      "form": "tablet",
      "dosagePerUnit": null,
      "unit": "mg",
      "instructions": "Принимать с едой",
      "totalQuantity": 20,
      "remainingQuantity": 20,
      "lowStockThreshold": 5,
      "trackStock": true,
      "iconName": "pill",
      "iconColor": "#FF0000",
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```

### Обновление медикамента
- **Метод**: `PATCH`
- **Путь**: `/api/medications/<id>/`
- **Описание**: Обновляет существующий медикамент (требуется аутентификация).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "name": "Ибупрофен",
      "form": "capsule",
      "unit": "mg",
      "instructions": "Принимать с едой",
      "totalQuantity": 15,
      "remainingQuantity": 15,
      "lowStockThreshold": 3,
      "trackStock": false,
      "iconName": "capsule",
      "iconColor": "#00FF00",
      "updatedAt": 1622548800000
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "1622548800002",
      "name": "Ибупрофен",
      "form": "capsule",
      "dosagePerUnit": null,
      "unit": "mg",
      "instructions": "Принимать с едой",
      "totalQuantity": 15,
      "remainingQuantity": 15,
      "lowStockThreshold": 3,
      "trackStock": false,
      "iconName": "capsule",
      "iconColor": "#00FF00",
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```

### Удаление медикамента
- **Метод**: `DELETE`
- **Путь**: `/api/medications/<id>/`
- **Описание**: Удаляет медикамент (требуется аутентификация).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)

### Получение списка расписаний
- **Метод**: `GET`
- **Путь**: `/api/schedules/`
- **Описание**: Возвращает список расписаний текущего пользователя.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  [
      {
          "id": "1622548800003",
          "medicationId": "1622548800001",
          "frequency": "daily",
          "days": [1, 2, 3],
          "dates": [],
          "times": [{"time": "08:00", "dosage": "200", "unit": "mg"}],
          "mealRelation": "before_meal",
          "startDate": "2023-01-01",
          "endDate": null,
          "durationDays": null,
          "createdAt": 1622548800000,
          "updatedAt": 1622548800000
      }
  ]
  ```

### Создание расписания
- **Метод**: `POST`
- **Путь**: `/api/schedules/`
- **Описание**: Создаёт новое расписание.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "id": "1622548800004",
      "medicationId": "1622548800001",
      "frequency": "daily",
      "mealRelation": "before_meal",
      "startDate": "2023-01-01",
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```
- **Ожидаемый ответ (201 Создано)**:
  ```json
  {
      "id": "1622548800004",
      "medicationId": "1622548800001",
      "frequency": "daily",
      "days": [],
      "dates": [],
      "times": [],
      "mealRelation": "before_meal",
      "startDate": "2023-01-01",
      "endDate": null,
      "durationDays": null,
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```

### Обновление расписания
- **Метод**: `PATCH`
- **Путь**: `/api/schedules/<id>/`
- **Описание**: Обновляет существующее расписание.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "medicationId": "1622548800001",
      "frequency": "daily",
      "mealRelation": "before_meal",
      "startDate": "2023-01-02",
      "updatedAt": 1622548800000
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "1622548800004",
      "medicationId": "1622548800001",
      "frequency": "daily",
      "days": [],
      "dates": [],
      "times": [],
      "mealRelation": "before_meal",
      "startDate": "2023-01-02",
      "endDate": null,
      "durationDays": null,
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000
  }
  ```

### Удаление расписания
- **Метод**: `DELETE`
- **Путь**: `/api/schedules/<id>/`
- **Описание**: Удаляет расписание.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)

### Получение списка приёмов
- **Метод**: `GET`
- **Путь**: `/api/intakes/`
- **Описание**: Возвращает список приёмов медикаментов текущего пользователя.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  [
      {
          "id": "1622548800005",
          "scheduleId": "1622548800004",
          "medicationId": "1622548800001",
          "scheduledTime": "12:00",
          "scheduledDate": "2023-01-01",
          "status": "taken",
          "takenAt": 1622548800000,
          "createdAt": 1622548800000,
          "updatedAt": 1622548800000,
          "medicationName": "Ибупрофен",
          "mealRelation": "before_meal",
          "dosagePerUnit": "200mg",
          "instructions": "Принимать с едой",
          "dosageByTime": "200",
          "unit": "mg",
          "iconName": "pill",
          "iconColor": "#FF0000"
      }
  ]
  ```

### Создание приёма
- **Метод**: `POST`
- **Путь**: `/api/intakes/`
- **Описание**: Регистрирует новый приём медикамента.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "id": "1622548800006",
      "scheduleId": "1622548800004",
      "medicationId": "1622548800001",
      "scheduledTime": "12:00",
      "scheduledDate": "2023-01-01",
      "status": "taken",
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000,
      "medicationName": "Ибупрофен",
      "mealRelation": "before_meal",
      "instructions": "Принимать с едой",
      "dosageByTime": "200",
      "unit": "mg",
      "iconName": "pill",
      "iconColor": "#FF0000"
  }
  ```
- **Ожидаемый ответ (201 Создано)**:
  ```json
  {
      "id": "1622548800006",
      "scheduleId": "1622548800004",
      "medicationId": "1622548800001",
      "scheduledTime": "12:00",
      "scheduledDate": "2023-01-01",
      "status": "taken",
      "takenAt": 1622548800000,
      "createdAt": 1622548800000,
      "updatedAt": 1622548800000,
      "medicationName": "Ибупрофен",
      "mealRelation": "before_meal",
      "dosagePerUnit": "200mg",
      "instructions": "Принимать с едой",
      "dosageByTime": "200",
      "unit": "mg",
      "iconName": "pill",
      "iconColor": "#FF0000"
  }
  ```

### Обновление приёма
- **Метод**: `PATCH`
- **Путь**: `/api/intakes/<id>/`
- **Описание**: Обновляет данные о приёме.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "status": "taken",
      "takenAt": 1622548900000,
      "updatedAt": 1622548900000
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "1622548800006",
      "scheduleId": "1622548800004",
      "medicationId": "1622548800001",
      "scheduledTime": "12:00",
      "scheduledDate": "2023-01-01",
      "status": "taken",
      "takenAt": 1622548900000,
      "createdAt": 1622548800000,
      "updatedAt": 1622548900000,
      "medicationName": "Ибупрофен",
      "mealRelation": "before_meal",
      "dosagePerUnit": "200mg",
      "instructions": "Принимать с едой",
      "dosageByTime": "200",
      "unit": "mg",
      "iconName": "pill",
      "iconColor": "#FF0000"
  }
  ```

### Удаление приёма
- **Метод**: `DELETE`
- **Путь**: `/api/intakes/<id>/`
- **Описание**: Удаляет запись о приёме.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)


## Управление настройками (`settings-store.ts`)

### Получение настроек уведомлений
- **Метод**: `GET`
- **Путь**: `/api/notifications/`
- **Описание**: Возвращает настройки уведомлений текущего пользователя.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  [
      {
          "id": "1622548800007",
          "medicationRemindersEnabled": true,
          "minutesBeforeScheduledTime": 15,
          "lowStockRemindersEnabled": true
      }
  ]
  ```

### Создание настроек уведомлений
- **Метод**: `POST`
- **Путь**: `/api/notifications/`
- **Описание**: Создаёт или обновляет настройки уведомлений (если они уже существуют).
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "medicationRemindersEnabled": true,
      "minutesBeforeScheduledTime": 30,
      "lowStockRemindersEnabled": false
  }
  ```
- **Ожидаемый ответ (201 Создано)**:
  ```json
  {
      "id": "1622548800008",
      "medicationRemindersEnabled": true,
      "minutesBeforeScheduledTime": 30,
      "lowStockRemindersEnabled": false
  }
  ```

### Обновление настроек уведомлений
- **Метод**: `PATCH`
- **Путь**: `/api/notifications/<user_id>/`
- **Описание**: Обновляет существующие настройки уведомлений.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Тело запроса (JSON)**:
  ```json
  {
      "medicationRemindersEnabled": false,
      "minutesBeforeScheduledTime": 10,
      "lowStockRemindersEnabled": true
  }
  ```
- **Ожидаемый ответ (200 OK)**:
  ```json
  {
      "id": "1622548800008",
      "medicationRemindersEnabled": false,
      "minutesBeforeScheduledTime": 10,
      "lowStockRemindersEnabled": true
  }
  ```

### Удаление настроек уведомлений
- **Метод**: `DELETE`
- **Путь**: `/api/notifications/<user_id>/`
- **Описание**: Удаляет настройки уведомлений.
- **Заголовки**:
  ```
  Authorization: Token your_token_here
  ```
- **Ожидаемый ответ (204 Нет содержимого)**: (пустой ответ)


## Дополнительные замечания

1. **Аутентификация**:
   - Все эндпоинты, кроме `/api/auth/users/`, `/api/auth/token/login/`, `/api/auth/users/reset_password/` и `/api/auth/users/reset_password_confirm/`, требуют заголовок `Authorization: Token your_token_here`.
   - Если токен отсутствует или недействителен, сервер вернёт ошибку `401 Неавторизован`.

2. **Обработка ошибок**:
   - Если пользователь попытается получить доступ к данным другого пользователя, сервер вернёт пустой список (или ошибку `403 Запрещено`, если фильтрация не сработает).
   - Например, запрос `GET /api/medications/` покажет только медикаменты текущего пользователя.

3. **Рекомендации для фронтенда**:
   - В `auth-store.ts` сохраняйте токен после входа и используйте его для всех последующих запросов.
