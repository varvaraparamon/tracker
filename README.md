# Трекер (Flask + SQLAlchemy)

Минималистичный тёмный веб‑интерфейс для оценивания команд и участников.

## Быстрый старт
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask --app app run  # первый запуск создаст пустую БД SQLite (если DATABASE_URL=sqlite:///tracker.db)
```

## Инициализация БД и данные
```bash
flask --app seed.py init-db
flask --app seed.py create-user admin SuperSecret123
flask --app seed.py demo-data
```

## Вход
Перейдите на /login и используйте выданные логин/пароль.

## UX / Валидации
- Кейс строго привязан к команде (как на фронте — через автоподстановку, так и на бэке — через проверку).
- Поле ФИО показывает только участников выбранной команды.
- Все выпадающие списки с поиском (Select2).
- Сообщения об ошибках/успехе через flash.
- Минималистичный тёмный UI без визуального шума.
```

