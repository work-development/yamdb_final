# Continuous Integration и Continuous Deployment для проекта YaMDB

<!-- ![yamdb_final workflow](https://github.com/work-development/yamdb_final/workflows/yamdb_final_workflow/badge.svg)  -->

### В этом проекте настроены:   

1. автоматический запуск тестов,      
2. обновление образов на Docker Hub,    
3. автоматический деплой на боевой сервер при пуше в главную ветку main.      

docker-compose.yaml настроен так, чтобы он разворачивал полноценное приложение на сервере с установленным docker.   

- В файл docker-compose.yaml описаны инструкции для трёх контейнеров: web, db, nginx,         
- Настроены volumes для базы данных, статики и медиа (файлов, загружаемых пользователями).    
         

### Workflow для репозитория yamdb_final на GitHub Actions      

Workflow описан в файле .github/workflows/yamdb_workflow.yml. В нём есть четыре job:     

- Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final.   
- Сборка и доставка докер-образов на Docker Hub.    
- Автоматический деплой проекта на боевой сервер.    
- Отправка уведомления в Telegram.    

### Подготовка сервера     

1. Установите службу nginx;   
2. Установите docker:    
```
sudo apt install docker.io
```
3. Установите docker-compose;    
4. Скопируйте подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.         
5. Добавьте в Secrets GitHub Actions переменные окружения для работы базы данных;        
