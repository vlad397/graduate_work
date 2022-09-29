# graduate_work_g
# Дипломный проект "Рекомендательная система"
### Описание
Система позволяет подобрать для пользователя фильмы, которые могли быть ему интересны, исходя из ранее просмотренных и оцененных.
<br/>
Используется content based подход, решающий алгоритм - поиск ближайших по косинусному расстоянию в пространстве эмбеддингов, полученных с помощью предобученной бертподобной сети 
### Ссылка
[Репозиторий](https://github.com/Chelovek760/graduate_work_g)
### Запуск
- C dev окружением:  
docker-compose -f docker-compose-dev.yml up
- С prod окружением:  
docker-compose up
- Поддерживаемая архитектура - х86
- Личный кабинет будет доступен по http://localhost:8002
- Film Сервис будет доступен по http://localhost:8003
- Документация
  - http://localhost:8002/api/docs
  - http://localhost:8003/api/docs
    <br/>
    <br/>
### Задачи
См. [issue](https://github.com/Chelovek760/graduate_work_g/issues?q=is%3Aissue+is%3Aclosed)

### Принципиальная схема работы
![alt text](https://github.com/vlad397/graduate_work/blob/main/docs/architecture.png)
<br/>
См. [Docs](https://github.com/vlad397/graduate_work/blob/main/docs/architecture.puml)
