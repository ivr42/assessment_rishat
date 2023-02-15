# ООО Ришат. Тестовое задание для Python разработчика
Оригинал тестового задания расположен по адресу: 

<https://docs.google.com/document/d/1RqJhk-pRDuAk4pH1uqbY9-8uwAqEXB9eRQWLSMM_9sI/>

## Стек технологий, использованных в проекте
- Docker
- PostgreSQL 13.0
- Python 3.10
- Django 4.1.6
- Django REST Framework (DRF) 3.14.0
- Stripe 5.1.1

## Использование
Образец сайта доступен по адресу <http://ivr.sytes.net:8080/>.
Endpoint-ы:
 - [item](http://ivr.sytes.net:8080/api/item/3/)
 - [buy](http://ivr.sytes.net:8080/api/buy/3/)

Сайт наполнен тестовыми данными.

Интерфейс администратора расположен по адресу <http://ivr.sytes.net:8080/admin/>,
<details>
<summary>Учётные данные</summary>

 - Имя пользователя: `djangoadmin`
 - Пароль пользователя: `ceiPiT8eiMisegie`

</details>

## Установка

Приложение разворачивается в инфраструктуре Docker следующей командой:
```bash
sudo docker-compose --file infra/docker-compose.yaml up -d --build
```
При первом запуске приложения создаются:
1. Служебная база данных (`postgress`)
2. Суперпользователь СУБД Postgresql (`postgress`)
3. База данных приложения
4. Выполняются миграции Django
5. Создаётся суперпользователь Django.
6. "Собирается" статика

## Переменные окружения
Все необходимые для работы приложения переменные окружения задаются в `.env` файле.

1. Переменные окружения, общие для контейнера базы данных и приложения:
    - `APP_DB_NAME` — имя базы данных приложения.
    - `APP_DB_USER` — пользователь с правами администратора на БД приложения.
    - `APP_DB_PASSWORD` — пароль для пользователя `APP_DB_USER`.

   В СУБД Postgres создаётся БД с именем `APP_DB_NAME` и пользователь
   `APP_DB_USER`, которому даются полные права на созданную БД.
   Django использует эти данные для доступа к БД.

2. Переменные окружения для контейнера СУБД Postgres:
    - `POSTGRES_DB` — Административная БД
    - `POSTGRES_USER` — Суперпользователь Postgres
    - `POSTGRES_PASSWORD` — Пароль суперпользователя Postgres

3. Переменные окружения для контейнера приложения **test_shop** (Django):

   Настройки Django:
   - `DJANGO_SECRET_KEY` —  [документация по SECRET_KEY](https://docs.djangoproject.com/en/4.1/ref/settings/#std:setting-SECRET_KEY)  
   - `DJANGO_DEBUG` — `True`/`False` — вкл/выкл режим отладки Django 

   Следующие переменные используются для настройки базы данных в Django:  
    - `DB_ENGINE` — Движок БД Django (по умолчанию — `django.db.backends.postgresql`)
    - `DB_HOST` — Хост БД (по умолчанию `db`)
    - `DB_PORT` — Порт для подключения к БД (по умолчанию `5432`)

   При инициализации приложения создаётся суперпользователь Django со следующими параметрами:
    - `DJANGO_SUPERUSER_USERNAME` — Имя пользователя для суперпользователя Django
    - `DJANGO_SUPERUSER_PASSWORD` — Пароль суперпользователя Django
    - `DJANGO_SUPERUSER_EMAIL` — e-mail суперпользователя Django

   Настройки Stripe
    - `STRIPE_PUBLIC_KEY` — Публичный ключ Stripe, передаётся во fronend
    - `STRIPE_SECRET_KEY` — Секретный ключ Stripe, используется в API

## Описание
[stripe.com/docs](http://stripe.com/docs) - платёжная система с подробным API и
бесплатным тестовым режимом для имитации и тестирования платежей. С помощью
python библиотеки `stripe` можно удобно создавать платежные формы разных видов,
сохранять данные клиента, и реализовывать прочие платежные функции. 
Мы предлагаем вам познакомиться с этой прекрасной платежной системой, реализовав
простой **сервер**, с одной html-страничкой, который общается со **Stripe** и
создает платёжные формы для товаров. 
Для решения нужно использовать **Django**. Решение бонусных задач даст вам
возможность прокачаться и показать свои умения, но это не обязательно. 

## Задание
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
 - Django Модель `Item` с полями (`name`, `description`, `price`)
 - API с двумя методами:
   - **GET** `/buy/{id}`, c помощью которого можно получить Stripe Session Id для оплаты выбранного `Item`. При выполнении этого метода c бэкенда с помощью python библиотеки `stripe` должен выполняться запрос `stripe.checkout.Session.create(...)` и полученный `session.id` выдаваться в результате запроса 
   - **GET** `/item/{id}`, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном `Item` и кнопка **Buy**. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки **Stripe** происходить редирект на Checkout форму `stripe.redirectToCheckout(sessionId=session_id)`
   - Пример реализации можно посмотреть в пунктах 1-3 [тут](https://stripe.com/docs/payments/accept-a-payment?integration=checkout)
 - Залить решение на Github, описать запуск в Readme.md
 Опубликовать свое решение чтобы его можно было быстро и легко протестировать. 
 Решения доступные только в виде кода на Github получат низкий приоритет при проверке.

## Бонусные задачи: 
 - Запуск используя Docker
 - Использование environment variables
 - Просмотр Django Моделей в Django Admin панели
 - Запуск приложения на удаленном сервере, доступном для тестирования
 - Модель `Order`, в которой можно объединить несколько `Item` и сделать платёж в **Stripe** на содержимое `Order` c общей стоимостью всех `Items`
 - Модели `Discount`, `Tax`, которые можно прикрепить к модели `Order` и связать с соответствующими атрибутами при создании платежа в **Stripe** - в таком случае они корректно отображаются в `Stripe Checkout`-форме. 
 - Добавить поле `Item.currency`, создать 2 `Stripe Keypair` на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
 - Реализовать не `Stripe Session`, а `Stripe Payment Intent`.

## Пример

API метод для получения HTML c кнопкой на платежную форму от **Stripe** для
`Item` с `id=1`: 
```shell
curl -X GET http://localhost:8000/item/1
```

Результат - HTML c инфой и кнопкой:
```html
<html>
<head>
   <title>Buy Item 1</title>
</head>
<body>
<h1>Item 1</h1>
<p>Description of Item 1</p>
<p>1111</p>
<button id="buy-button">Buy</button>
<script type="text/javascript">
      var stripe = Stripe('pk_test_a9nwZVa5O7b0xz3lxl318KSU00x1L9ZWsF');
      var buyButton = document.getElementById(buy-button');
      buyButton.addEventListener('click', function() {
        // Create a new Checkout Session using the server-side endpoint 
        // Redirect to Stripe Session Checkout
        fetch('/buy/1', {method: 'GET'})
        .then(response => return response.json())
        .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
      });
    </script>
</body>
</html>
```
