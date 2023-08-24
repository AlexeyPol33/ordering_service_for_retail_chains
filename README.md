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


## API Endpoints

### Аутентификация и управление аккаунтом

<details>
<summary>api/user/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/user/contact/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/token/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/token/refresh/</summary>

Скрытый текст здесь...

</details>

### Управление корзиной и заказами

<details>
<summary>api/order/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/orderitem/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/order/confirm//</summary>

Скрытый текст здесь...

</details>

### Управление продуктами
<details>
<summary>api/product/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/productinfo/</summary>

Скрытый текст здесь...

</details>

### Управление магазином

<details>
<summary>api/shop/</summary>

Скрытый текст здесь...

</details>

<details>
<summary>api/shop/upload/</summary>

Скрытый текст здесь...

</details>


## Особые команды сервера

<details>
<summary>python manage.py load_yaml_data</summary>

Команда предназначена для загрузки yaml файла в базу данных.

флаги:

 -p, --path указывает путь к файлу, по умолчанию ищет файлы .yaml в коренной директории.

 -u, --user назначает пользователя владельцем магазина из файла

</details>

