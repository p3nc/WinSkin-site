# WinSkin

WinSkin — це веб-додаток на базі Flask, який реалізує ігрову платформу для отримання віртуальних скінів через механіку рулетки. Користувачі можуть реєструватися, входити в систему, поповнювати баланс тугриків, обертати рулетку для виграшу скінів та керувати своїм інвентарем. Адміністратори мають доступ до панелі для додавання та видалення скінів. Додаток включає інтерактивний клієнтський інтерфейс з анімаціями та підказками.

## Структура проєкту
```
project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── roulette.py
│   │   ├── admin.py
│   │   ├── main.py
│   │   ├── user.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   │   ├── roulette.js
│   │   │   ├── user.js
│   │   │   ├── mainpage.js
│   │   ├── images/
│   │       ├── Case1_Revolution/
│   │       ├── Case2_Kilowatt/
│   │       ├── Case3_DangerZone/
│   ├── templates/
│       ├── base.html
│       ├── roulette.html
│       ├── 403.html
│       ├── admin_skins.html
│       ├── inventory.html
│       ├── login.html
│       ├── registration.html
│       ├── user.html
│       ├── mainpage.html
├── migrations/
├── venv/
├── instance/
├── requirements.txt
├── config.py
├── run.py
├── .gitignore
```

## Основні функції
- **Аутентифікація**: Реєстрація, вхід, вихід із відправкою вітального листа через Gmail SMTP.
- **Користувацький профіль**: Перегляд профілю, поповнення балансу тугриків (1–1000), перегляд інвентарю скінів.
- **Рулетка**: Обертання за 100 тугриків із випадковим вибором скіна (ймовірності: blue 50%, green 20%, purple 15%, pink 10%, red 4%, yellow 1%). Підтримка трьох колекцій: Revolution, Kilowatt, DangerZone.
- **Адмін-панель**: Додавання та видалення скінів із підтримкою зображень (доступ лише для адміністраторів).
- **Інтерактивність**: Анімація рулетки, ефект розбиття кнопки на сторінці профілю, циклічні підказки на головній сторінці.

## Вимоги до системи
- **Апаратне забезпечення**: 2 ГБ ОЗУ, 500 МБ дискового простору.
- **Операційна система**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+).
- **Програмне забезпечення**: Python 3.8+, сучасний браузер.
- **Залежності** (вказані в `requirements.txt`):
  - `flask`
  - `flask-sqlalchemy`
  - `flask-mail`
  - `werkzeug`
- **Сервіси**: Gmail SMTP для відправки листів.
- **Статичні файли**: Зображення для кейсів у `app/static/images/` (`Case1_Revolution`, `Case2_Kilowatt`, `Case3_DangerZone`).

## Встановлення

1. **Клонувати проєкт**:
   - Клонувати репозиторій або скопіювати файли до директорії `project`:
     ```bash
     git clone <URL_репозиторію>
     cd project
     ```

2. **Створити віртуальне середовище**:
   - Виконати:
     ```bash
     python -m venv venv
     ```
   - Активувати:
     - Linux/macOS: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`

3. **Встановити залежності**:
   - Переконатися, що `requirements.txt` містить:
     ```
     flask
     flask-sqlalchemy
     flask-mail
     werkzeug
     ```
   - Встановити:
     ```bash
     pip install -r requirements.txt
     ```

4. **Налаштувати структуру директорій**:
   - Створити директорію `instance`, якщо відсутня:
     ```bash
     mkdir instance
     ```
   - Переконатися, що зображення для кейсів знаходяться в `app/static/images/`.
   - Перевірити наявність JS-файлів у `app/static/js/` та шаблонів у `app/templates/`.

5. **Ініціалізувати базу даних**:
   - У Python-консолі виконати:
     ```bash
     python
     >>> from app import db, create_app
     >>> app = create_app()
     >>> with app.app_context():
     ...     db.create_all()
     >>> exit()
     ```
   - Це створить `instance/db.sqlite` із таблицями `user`, `skin`, `inventory`.

6. **Розмістити статичні файли**:
   - Скопіювати зображення до `app/static/images/Case1_Revolution/`, `app/static/images/Case2_Kilowatt/`, `app/static/images/Case3_DangerZone/`.
   - Переконатися, що `roulette.js`, `user.js`, `mainpage.js` знаходяться в `app/static/js/`.

7. **Запустити тестовий режим**:
   - Виконати:
     ```bash
     python run.py
     ```
   - Відкрити `http://127.0.0.1:5000` у браузері.

## Конфігурація

1. **Оновити `config.py`**:
   - Згенерувати унікальний `SECRET_KEY`:
     ```python
     import os
     SECRET_KEY = os.urandom(24).hex()
     ```
   - Налаштувати Gmail SMTP:
     - Отримайте App Password у Google Account (https://myaccount.google.com/security).
     - Вказати в `config.py`:
       ```python
       MAIL_USERNAME = 'your_email@gmail.com'
       MAIL_PASSWORD = 'your_app_password'
       ```
   - Перевірити шлях до бази даних: `sqlite:///instance/db.sqlite`.

2. **Використати змінні середовища** (рекомендується):
   - Встановити `python-dotenv`:
     ```bash
     pip install python-dotenv
     ```
   - Створити файл `.env` у корені проєкту:
     ```
     MAIL_USERNAME=your_email@gmail.com
     MAIL_PASSWORD=your_app_password
     SECRET_KEY=your_random_secret_key
     ```
   - Додати до `config.py`:
     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

3. **Продакшен (опціонально)**:
   - Встановити Gunicorn:
     ```bash
     pip install gunicorn
     ```
   - Запустити:
     ```bash
     gunicorn -w 4 -b 0.0.0.0:8000 run:app
     ```
   - Налаштувати Nginx як реверс-проксі:
     ```nginx
     server {
         listen 80;
         server_name your_domain;
         location / {
             proxy_pass http://127.0.0.1:8000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```
   - Увімкнути HTTPS через Let’s Encrypt.

## Тестування

### Види тестування
- **Функціональне**: Перевірка сценаріїв (реєстрація, вхід, обертання рулетки, адмін-панель).
- **Модульне**: Тестування функцій у `auth.py`, `roulette.py`, `roulette.js` (наприклад, `set_password`, `determineWinner`).
- **Інтеграційне**: Перевірка API (`/roulette/spin`, `/roulette/save`, `/user/api/get_balance`) та взаємодії з базою даних.
- **Системне**: Наскрізні тести (реєстрація → вхід → рулетка → інвентар).

### Методи тестування
- **Чорна скринька**: Перевірка користувацьких сценаріїв через інтерфейс.
- **Біла скринька**: Тестування логіки окремих функцій із урахуванням коду.
- **Інтеграційне тестування API**: Перевірка коректності API-запитів.
- **Наскрізне тестування**: Імітація повних користувацьких сценаріїв.

### Метрики тестування
- **Покриття коду**: ≥80% для критичних модулів (`auth.py`, `roulette.py`, `roulette.js`), ≥60% для некритичних (`mainpage.js`).
- **Щільність дефектів**: <5 дефектів на 1000 рядків коду для критичних модулів, <10 для некритичних.
- **Ефективність тестування**: ≥90% для критичних дефектів, ≥70% для всіх.

### Інструменти тестування
- **Pytest**: Для модульного тестування Python-коду.
- **Jest**: Для тестування JavaScript-коду.
- **Postman**: Для тестування API-запитів.
- **Selenium/Cypress**: Для наскрізного тестування.
- **Coverage.py**: Для вимірювання покриття коду Python.
- **TestRail**: Для управління тест-кейсами та дефектами.
- **Flake8/ESLint**: Для перевірки якості коду.

### Приклад тест-кейсу
- **Назва**: Реєстрація з існуючим email.
- **Тип**: Функціональне, чорна скринька.
- **Опис**: Спробувати зареєструватися з email, який уже є в базі.
- **Очікуваний результат**: Повідомлення "Email already registered" та перенаправлення на `/registration`.
- **Інструмент**: Ручне тестування або Selenium.

## Усунення проблем
- **Помилка модулів**: Перевірте встановлення залежностей (`pip install -r requirements.txt`).
- **Проблеми з базою даних**: Переконайтеся, що `instance/db.sqlite` створено (`db.create_all()`).
- **Проблеми з email**: Перевірте `MAIL_USERNAME`, `MAIL_PASSWORD` та App Password у Gmail.
- **Статичні файли не завантажуються**: Переконайтеся, що зображення та JS-файли доступні в `app/static/`.
- **Помилка 403**: Перевірте, чи користувач має права адміністратора для доступу до адмін-панелі.

## Контакти
Для запитань або пропозицій звертайтеся:
- Email: denys.zlyvko@student.karazin.ua
- Email: ivan.kohutenko@student.karazin.ua
- Email: serhii.travchenko@student.karazin.ua
