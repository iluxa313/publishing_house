# Publishing House

**Publishing House** — веб-приложение для научного издательства, позволяющее публиковать статьи в журналах различных областей науки. Разработано на Django.

## Функционал
- 📝 Публикация статей (для администраторов)
- 💬 Комментарии к статьям (для авторизированных пользователей)
- 🔐 Авторизация и регистрация пользователей
- 📑 Пагинация постов
- 📌 Социальные функции (лента публикаций, взаимодействие с контентом)

## Технологии
- Python 3.x
- Django
- SQLite (или другая БД, в зависимости от настроек)
- HTML/CSS (шаблоны Django)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/iluxa313/publishing_house.git
cd publishing_house
```

### 2. Настройка виртуального окружения
```bash 
python -m venv venv
```

### 3. Активация окружения:
Windows:

```bash
.\venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Установка зависимостей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка БД
```bash
python manage.py migrate
```

### 5. Создание администратора (опционально)
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера
```bash
python manage.py runserver
```

Откройте в браузере: http://127.0.0.1:8000/
