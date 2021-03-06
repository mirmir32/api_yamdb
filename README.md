# Групповой проект. Спринт 10. Яндекс.Практикум.
## Описание
#### YaMDB 
* API для учебного проекта YaMDB - учебного проекта соц.сети, в котором пользователи могут размещать обзоры на произведения в разных категориях (фильмы, музыка, кино) и жанрах, после чего на основании оценок формируется рейтинг произведений. 
* API позволяет: 
- регистрироваться пользователям;
- управлять списком категорий, жанров, произведений;
- получать, размещать изменять и удалять отзывы, комментарии к ним;
- а еще у нас есть рейтинг произведений и неплохая админка!
* Скоро релиз!

## Установка 
Клонируем репозиторий:

```$ git clone https://github.com/mirmir32/api_yamdb.git```
 
 Создаем виртуальное окружение:
 
 ```$ python -m venv venv```
 
 Устанавливаем зависимости:
 
```$ pip install -r requirements.txt```

Создание и применение миграций:

```$ python manage.py makemigrations``` и ```$ python manage.py migrate```

Запускаем django сервер:

```$ python manage.py runserver```

Успех! Вы восхитительны!

## Документация к API:

После запуска проекта 

по адресу `http://127.0.0.1:8000/redoc/` доступна документация для API **YaMDB**.
