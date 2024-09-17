<div id="header" align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWd2MmhmazA4NnNmaTY3OHJzNnJ0ZjJuYnM1N3N3NnZ1cDM5eGsyMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UQ25FULQkgfwALbzpR/giphy.gif" width="3000"/>
</div>

# Тестовое задание Tevian

## Постановка задачи

Необходимо разработать сервис с REST API на основе HTTP с передачей данных в формате JSON. Сервис должен вести список заданий (Task). В задание загружаются изображения (Image). С помощью стороннего сервиса на изображениях необходимо найти лица (Face), определить их пол и возраст. На основе полученных данных в рамках задания нужно получить статистики.


### Установка и Запуск
- установите Docker по ссылке https://www.docker.com/products/docker-desktop/
- запустите Docker
- создайте файл .env с данными по образу в [.env.example](.env.example)
- запустите терминал и по очереди введите команды написанные в поле ниже
```bash
git clone <URL_репозитория> # клонирование репозитория
cd <папка_репозитория> # переход в локальный репозиторий
docker-compose up --build # запуск всех сервисов
```
Swagger Fast_API будет доступен по [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Для выключения процесса Docker нажмите CTL+C
### Документация API:

**Для доступа к конечным точкам c помощью swagger авторизуйтесь!**
1. Зайдите в документацию.
2. В поле **Authorization** введите логин и пароль, указанные в файле `.env`:
   - **USERNAME**: `username`
   - **PASSWORD**: `password`


### API Endpoints

#### Endpoint: `POST /create_new_task`
##### (Добавление задания)
Введите название задания который хотите создать.
В ответе вы получите json, запомните параметр id он понадобится для ручки /load_images и /get_task.

**Example Response**:

```json
{
  "male_female_faces": 0,
  "average_age_male": 0,
  "name": "Test",
  "all_faces": 0,
  "average_age_female": 0,
  "id": "03411e19-c3f7-4994-9a26-b097f1acec8d",
  "images": []
}
```

#### Endpoint: `POST /load_images`
##### (Добавление изображения в задание)
Вместе с изображением передается его название и uuid задачи (поле id, я советовал запомнить его в ручке /create_new_task) к которому необходимо привязать изображение. Изображение учитывается в статистике в запросе "Получение задания" сразу после завершения запроса.

**Example Response**:

```json
{
  "info ": "info ": "The image has been processed and added to the task"
}
```

#### Endpoint: `DELETE /delete_task_use_id`
##### (Удаление задания)
 При удалении задания все связанные с ним данные будут удалены.

**Example Response**:

```json
{
   "info ": "Task deleted"
}
```

#### Endpoint: `GET /get_task`
##### (Получение задания)
Введите id задачи (поле id которое я советовал запомнить в ручке /create_new_task) для получения ответа.
В ответе на запрос будут:
* Идентификатор задания.
* Список изображений в задании, содержащий для каждого изображения:
  * Его название.
  * Список лиц, найденных на изображении, содержащий для каждого
лица:
    * Bounding box лица.
    * Пол.
    * Возраст.
  * Суммарное число лиц на всех изображениях в задании.
  * Суммарное число мужчин и женщин на всех изображениях в задании.
  * Средний возраст мужчин на всех изображениях в задании.
  * Средний возраст женщин на всех изображениях в задании.

**Example Response**:

```json
{
  "task_id": "95c16aeb-3fbb-4408-ba73-7c3ce010e07b",
  "images": [
    {
      "name": "Test_Image",
      "faces": [
        {
          "bounding_box": {
            "height": 385,
            "width": 298,
            "x": 507,
            "y": 276
          },
          "gender": "male",
          "age": 25
        }
      ]
    }
  ],
  "total_faces": 1,
  "male_count": 1,
  "female_count": 0,
  "average_age_male": 25,
  "average_age_female": 0
}
```

- Все вопросы можно задать автору по ссылке: [![Telegram Badge](https://img.shields.io/badge/-telegram-blue?style=flat&logo=Telegram&logoColor=white)](https://t.me/Neighbourhood99)