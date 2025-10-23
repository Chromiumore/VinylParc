# Запуск веб-приложения
1. Создать и заполнить .env файл в папке backend  
Пример заполнения:
>DB_HOST="localhost"  # Хост сервера с базой данных POSTGRES  
>DB_PORT=5432  # Порт сервера с базой данных POSTGRES  
>DB_NAME="vinyl"  # Имя сервера с базой данных POSTGRES  
>DB_USER="postgres"  # Имя пользователя базы данных POSTGRES  
>DB_PASSWORD=12345  # Пароль для подключения к базе данных POSTGRES  
>  
>AUTH_SECRET_KEY='SECRET'  # Секретный ключ для авторизации  

2. Создать виртуальное окружение в папке backend, запустить из папки backend, установить нужные библиотеки выполнив команду:
>pip install -r requirements.txt  

3. Запустить сервер командой из папки backend:
> uvicorn app.main:create_app --reload --factory

# Запуск docker-compose
1. Создать файл .env.compose в корне проекта и заполнить подобно .env

**ВАЖНО!!!!!**

>DB_HOST="postgres"

**!!!!**

2. Выполнить команду для запуска контейнера из корня проекта:
> docker-compose up --build

3. Применить миграции к бд с запущенным контейнером
> docker exec -it vinyl-parc-backend-1 alembic upgrade head

![Прикол](https://i.pinimg.com/736x/aa/78/66/aa78667a89d0a8bfee78e43251107b4a.jpg)