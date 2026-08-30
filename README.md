# Blogicum - блог-платформа

## Описание проекта

**Blogicum** - это блог-платформа для публикации постов и их обсуждения. Пользователи могут:
- регистрироваться и авторизовываться в системе;
- создавать, редактировать и удалять собственные публикации;
- указывать для публикаций категорию и местоположение;
- комментировать записи других авторов;
- загружать изображения к постам.

Реализована система отложенных публикаций, пагинация и кастомные страницы ошибок.

## Стек технологий

- **Бэкенд:** Python 3.12, Django 5;
- **База данных:** SQLite;
- **ORM:** Django ORM;
- **Аутентификация:** Django Authentication System;
- **Работа с изображениями:** Pillow;
- **Фронтенд:** HTML, CSS (шаблоны Django);
- **Инструменты:** Git, GitHub, pytest, flake8.

---

## Как запустить проект

### 1. Клонируйте репозиторий и перейдите в него в командной строке

```
git clone https://github.com/russinArtem/blogicum.git
cd blogicum
```

### 2. Создайте и активируйте виртуальное окружение

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас Windows

    ```
    source venv/Scripts/activate
    ```

### 3. Обновите пакетный менеджер `pip` и установите зависимости из файла `requirements.txt`

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

### 4. Выполните миграции

```
python3 manage.py migrate
```

### 5. Запустите сервер разработки

```
python3 manage.py runserver
```

Проект будет доступен по адресам:
- [Сайт](http://127.0.0.1:8000/)
- [Админ-панель](http://127.0.0.1:8000/admin/)

---

## Автор

**Артем Руссин**

GitHub: [russinArtem](https://github.com/russinArtem/)

Email: [russinartem@yandex.ru](mailto:russinartem@yandex.ru)

## Лицензия

Проект выполнен в рамках учебного курса [Яндекс.Практикум](https://practicum.yandex.ru/).
