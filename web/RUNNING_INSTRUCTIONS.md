# Инструкции по запуску Tic-Tac-Toe API

## Предварительные требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

## Установка

### 1. Установите зависимости

```bash
pip install flask
```

### 2. Структура проекта

Убедитесь, что у вас есть следующая структура проекта:

```
tic-tac-toe/
├── domain/              # Domain слой (бизнес-логика)
│   ├── model/
│   └── service/
├── datasource/          # Datasource слой (хранение данных)
│   ├── model/
│   ├── mapper/
│   └── repository/
├── web/                 # Web слой (REST API)
│   ├── model/
│   ├── mapper/
│   ├── route/
│   └── module/
└── main.py             # Точка входа
```

**Примечание:** Domain и Datasource слои должны быть реализованы согласно заданиям 2 и 3. В поставке включены только файлы web-слоя.

## Запуск сервера

### Вариант 1: Простой запуск

```bash
python main.py
```

Сервер запустится на `http://localhost:5000`

Вывод в консоли:
```
Starting Tic-Tac-Toe API server...
Server running at http://localhost:5000

Endpoints:
  POST /game/{uuid} - Submit move and get computer response
  GET  /health      - Health check

Press Ctrl+C to stop
```

### Вариант 2: Настройка параметров

Отредактируйте `main.py`:

```python
# Изменить host
run_app(game_service, host='127.0.0.1', port=5000, debug=True)

# Изменить port
run_app(game_service, host='0.0.0.0', port=8080, debug=True)

# Отключить debug режим (для production)
run_app(game_service, host='0.0.0.0', port=5000, debug=False)
```

## Проверка работоспособности

### 1. Health Check

```bash
curl http://localhost:5000/health
```

Ожидаемый ответ:
```json
{
  "status": "ok"
}
```

### 2. Тест игры

```bash
curl -X POST http://localhost:5000/game/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "board": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
  }'
```

Ожидаемый ответ:
```json
{
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "board": [
    [2, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
  ]
}
```

## Запуск тестов

### Тесты web-слоя

```bash
python tests/web/test_web.py
```

Ожидаемый вывод:
```
======================================================================
WEB LAYER TESTS
======================================================================

Testing Web Models...
✓ WebGameBoard created
✓ Board to_dict works
✓ Board from_dict works
✓ WebGame created
...

======================================================================
ALL WEB LAYER TESTS PASSED! ✓
======================================================================
```

### Примеры использования API

```bash
python examples/api_examples.py
```

**Важно:** Сервер должен быть запущен перед выполнением примеров!

## Использование API

### Создание новой игры

1. Сгенерируйте UUID для игры (можно использовать любой UUID генератор)
2. Сделайте первый ход (человек играет за X, значение 1)
3. Отправьте POST запрос на `/game/{uuid}`

### Продолжение существующей игры

1. Используйте тот же UUID
2. Сделайте следующий ход (добавьте одну клетку со значением 1)
3. Отправьте POST запрос с обновленной доской

### Значения клеток доски

- `0` - Пустая клетка
- `1` - X (ход человека)
- `2` - O (ход компьютера)

## Примеры использования

### Python (requests)

```python
import requests
from uuid import uuid4

# Создать новую игру
game_id = uuid4()

# Человек играет в центре
response = requests.post(
    f'http://localhost:5000/game/{game_id}',
    json={
        'uuid': str(game_id),
        'board': [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    }
)

# Получить ответ компьютера
result = response.json()
print(f"Computer played: {result['board']}")
```

### JavaScript (fetch)

```javascript
const gameId = '123e4567-e89b-12d3-a456-426614174000';

fetch(`http://localhost:5000/game/${gameId}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    uuid: gameId,
    board: [
      [0, 0, 0],
      [0, 1, 0],
      [0, 0, 0]
    ]
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Обработка ошибок

API возвращает детальные сообщения об ошибках:

### Невалидный ход

```json
{
  "error": "Invalid move",
  "message": "Multiple cells changed: 2. Only one move allowed per turn."
}
```

### Несоответствие UUID

```json
{
  "error": "UUID mismatch",
  "message": "UUID in URL (...) does not match UUID in body (...)"
}
```

### Игра завершена

```json
{
  "error": "Game already over",
  "message": "Human wins (X)"
}
```

## Остановка сервера

Нажмите `Ctrl+C` в терминале где запущен сервер.

## Решение проблем

### Порт уже используется

Если порт 5000 занят:
1. Измените порт в `main.py`
2. Или остановите процесс, использующий порт 5000

```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### ModuleNotFoundError

Убедитесь, что:
1. Все слои проекта (domain, datasource, web) находятся в правильных директориях
2. Python путь настроен корректно
3. Все `__init__.py` файлы созданы

### Flask не установлен

```bash
pip install flask
```

или

```bash
pip install -r requirements.txt
```

## Production развертывание

Для production используйте WSGI сервер, например Gunicorn:

```bash
# Установить Gunicorn
pip install gunicorn

# Запустить с Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "web.module.app:create_app(game_service)"
```

## Дополнительная информация

- **Документация API**: См. `web/WEB_LAYER.md`
- **Примеры**: См. `examples/api_examples.py`
- **Тесты**: См. `tests/web/test_web.py`

## Контакты

При возникновении проблем обратитесь к документации:
- `web/README.md` - Быстрый старт
- `web/WEB_LAYER.md` - Полная документация
- `TASK_4_COMPLETION_REPORT.md` - Итоговый отчет
