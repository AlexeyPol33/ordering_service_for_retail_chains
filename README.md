# API Service for ordering goods for retail chains

## Введение
Приложение предназначено для автоматизации закупок в розничной сети. Пользователи сервиса — покупатель (менеджер торговой сети, который закупает товары для продажи в магазине) и поставщик товаров.

## Оглавление
- [API Service for ordering goods for retail chains](#api-service-for-ordering-goods-for-retail-chains)
  - [Введение](#введение)
  - [Оглавление](#оглавление)
  - [API Endpoints](#api-endpoints)
    - [Аутентификация и управление аккаунтом](#аутентификация-и-управление-аккаунтом)
    - [Управление корзиной и заказами](#управление-корзиной-и-заказами)
    - [Управление продуктами](#управление-продуктами)
    - [Управление магазином](#управление-магазином)
  - [Особые команды сервера](#особые-команды-сервера)
  - [Docker](#docker)
  - [Тесты](#тесты)


## API Endpoints

### Аутентификация и управление аккаунтом

<details>
<summary> api/user/</summary>
  <details>
  <summary>[GET] api/user/(id) - Просмотр профиля</summary>
  Скрытый текст
  </details>
  <details>
  <summary>[POST] api/user/ - Регистрация нового пользователя</summary>
  Скрытый текст
  </details>
  <details>
  <summary>[PATCH] api/user/(id) - Обновление учетных данных </summary>
  Скрытый текст
  </details>
  <details>
  <summary> [DELETE] api/user/(id) - Удаление учетной записи </summary>
  </details>
</details>

<details>
<summary>/social/login/</summary>

  - /social/login/vk-oauth2/ - Для регистрации и входа через вк
  - /social/login/google-oauth2/ - Для регистрации и входа через Google
</details>

<details>
<summary>api/user/contact/</summary>
  <details>
  <summary>[GET] api/user/contact/(id) - Посмотреть контактную информацию</summary>
  TEXT
  </details>
  <details>
  <summary>[PATCH] api/user/contact/(id) - Обновить контактную информацию</summary>
  TEXT
  </details>

</details>

<details>
<summary>api/token/</summary>
  <details>
  <summary>[POST] api/token/ -Получить токены </summary>
  TEXT
  </details>
</details>

<details>
<summary>api/token/refresh/</summary>
  <details>
  <summary>[POST] api/token/refresh/ - Обновить токен</summary>
  TEXT
  </details>
</details>

### Управление корзиной и заказами

<details>
<summary>api/order/</summary>
  <details>
  <summary>[GET] api/order/ - Посмотреть заказы</summary>
  TEXT
  </details>
</details>

<details>
<summary>api/orderitem/</summary>
  <details>
  <summary>[GET] api/orderitem/ - Посмотреть предметы заказов</summary>
  TEXT
  </details>
  <details>
  <summary>[POST] api/orderitem/ - Добавить предмет в корзину</summary>
  TEXT
  </details>

  <details>
  <summary>[DELETE] api/orderitem/ - Удалить предмет из корзины</summary>
  TEXT
  </details>
</details>

<details>
<summary>api/order/confirm/</summary>
 
  <details>
  <summary>[POST] api/order/confirm/ - Подтвердить заказ</summary>
  TEXT
  </details>

</details>

### Управление продуктами
<details>
<summary>api/product/</summary>
  <details>
  <summary>[GET] api/product/ - Получить список продуктов</summary>
  TEXT
  </details>
  <details>
  <summary>[POST] api/product/ - Добавить продукт</summary>
  TEXT
  </details>
  <details>
  <summary>[PATCH] api/product/(id) - Изменить продукт</summary>
  TEXT
  </details>
  <details>
  <summary>[DELETE] api/product/(id) - удалить продукт</summary>
  TEXT
  </details>
</details>

<details>
<summary>api/productinfo/</summary>
  <details>
  <summary>[GET] api/productinfo/(id) - Получить информацию о продукте </summary>
  TEXT
  </details>
  <details>
  <summary>[PATCH] api/productinfo/(id) - Изменить информацию о проекте</summary>
  TEXT
  </details>
</details>

### Управление магазином

<details>
<summary>api/shop/</summary>
  <details>
  <summary>[GET] api/shop/ - Получить список магазинов</summary>
  TEXT
  </details>
  <details>
  <summary>[PATCH] api/shop/ - Обновить информацию о магазине</summary>
  TEXT
  </details>
</details>

<details>
<summary>api/shop/upload/</summary>

<details>
<summary>[POST] /shop/upload/     - Загрузить файл на сервер</summary>  

- Authorization: Bearer

- Content-Type: multipart/form-data

- Content-Disposition: attachment; filename=shop.yaml
</details>

</details>


## Особые команды сервера

<details>
<summary>python manage.py load_yaml_data</summary>

Команда предназначена для загрузки yaml файла в базу данных.

флаги:

 -p, --path указывает путь к файлу, по умолчанию ищет файлы .yaml в коренной директории.

 -u, --user назначает пользователя владельцем магазина из файла

</details>

## Docker
<details>
<summary> docker-compose up --build </summary>
</details>

## Тесты
pytest --cov=app --cov-config=.coveragerc