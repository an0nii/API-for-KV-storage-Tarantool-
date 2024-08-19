# API-for-KV-storage-Tarantool-
**VK Internship Project**

## Инструкции по запуску вашего решения

1. **Клонируйте репозиторий:**
   ```sh
   git clone <URL вашего репозитория>
   cd <название вашего репозитория>
   ```

2. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Запустите приложение:**
   ```sh
   docker-compose up --build
   ```
   
**Чтобы выключить приложение:**
   ```sh
   docker-compose down
   ```

## Полная документация к API

### `POST /api/register`

**Описание:** Регистрация нового пользователя.

**Пример запроса UNIX:**
```sh
curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}'
```

**Пример запроса Windows:**
```sh
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    "username" = "new_user"
    "password" = "new_password"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/register -Method Post -Headers $headers -Body $body
```

**Пример ответа:**
```json
{
  "status": "User created successfully"
}
```

**Ошибки:**
- `400 Bad Request`: Имя пользователя и пароль обязательны.
- `409 Conflict`: Пользователь уже существует.

### `POST /api/login`

**Описание:** Аутентификация пользователя и получение токена.

**Пример запроса UNIX:**
```sh
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"username": "new_user", "password": "new_password"}'
```
**Пример запроса Windows:**
```sh
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    "username" = "new_user"
    "password" = "new_password"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri http://localhost:5000/api/login -Method Post -Headers $headers -Body $body
$token = $response.token
```

**Пример ответа:**
```json
{
  "token": "your_jwt_token"
}
```

**Ошибки:**
- `401 Unauthorized`: Неверные учетные данные.

### `POST /api/write`

**Описание:** Запись данных в базу данных.

**Пример запроса UNIX:**
```sh
curl -X POST http://localhost:5000/api/write -H "Content-Type: application/json" -H "Authorization: Bearer your_jwt_token" -d '{"data": {"key1": "value1", "key2": "value2", "key3": 1}}'
```

**Пример запроса Windows:**
```sh
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $token"
}

$body = @{
    "data" = @{
        "key1" = "value1"
        "key2" = "value2"
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/write -Method Post -Headers $headers -Body $body
```

**Пример ответа:**
```json
{
  "status": "success"
}
```

**Ошибки:**
- `400 Bad Request`: Данные не предоставлены.
- `403 Forbidden`: Неверный токен.
- `500 Internal Server Error`: Внутренняя ошибка сервера.

### `POST /api/read`

**Описание:** Чтение данных из базы данных.

**Пример запроса UNIX:**
```sh
curl -X POST http://localhost:5000/api/read -H "Content-Type: application/json" -H "Authorization: Bearer your_jwt_token" -d '{"keys": ["key1", "key2", "key3"]}'
```

**Пример запроса Windows:**
```sh
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $token"
}

$body = @{
    "keys" = @("key1", "key2")
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/read -Method Post -Headers $headers -Body $body
```

**Пример ответа:**
```json
{
  "data": {
    "key1": "value1",
    "key2": "value2",
    "key3": 1
  }
}
```

**Ошибки:**
- `400 Bad Request`: Ключи не предоставлены.
- `403 Forbidden`: Неверный токен.