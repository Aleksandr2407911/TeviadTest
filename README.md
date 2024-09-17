<div id="header" align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWd2MmhmazA4NnNmaTY3OHJzNnJ0ZjJuYnM1N3N3NnZ1cDM5eGsyMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UQ25FULQkgfwALbzpR/giphy.gif" width="3000"/>
</div>

# Тестовое задание Tevian

## Постановка задачи

Необходимо разработать сервис с REST API на основе HTTP с передачей данных в формате JSON. Сервис должен вести список заданий (Task). В задание загружаются изображения (Image). С помощью стороннего сервиса на изображениях необходимо найти лица (Face), определить их пол и возраст. На основе полученных данных в рамках задания нужно получить статистики.


## Установка и Запуск
### Процесс установки и запуска происходит на Windows, при необходимости будет написана нструкция для Linux.
- установите Docker по ссылке https://www.docker.com/products/docker-desktop/
- запустите Docker
- установите git bash по ссылке https://gitforwindows.org/ (можно использовать bash в редакторе кода)
- создай файл .env с данными по образу в [.env.example](.env.example)
- запустите git bash и по очереди введите команды написанные в поле ниже
```bash
git clone <URL_репозитория> # клонирование репозитория
cd <папка_репозитория> # переход в локальный репозиторий
docker-compose up --build # запуск всех сервисов
```
API будет доступен по [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Документация API: 

Для доступа к конечным точкам c помощью swagger **авторизуйтесь**:
1. Зайдите в документацию.
2. В поле **Authorization** введите логин и пароль, указанные в файле `.env`:
   - **USERNAME**: `aleksandr`
   - **PASSWORD**: `coder1170`


### API Endpoints

#### Create New Task (Добавление задания)

**Endpoint**: `POST /create_new_task`

**CURL**:
```
curl -X POST http://127.0.0.1:8000/tevian_test/create_new_task \
     -H "Content-Type: application/json" \
     -H "Authorization: Basic YWxla3NhbmQ6Y29kZXIxMTcw" \
     -d '{
           "name": "Новая задача"
         }'
```

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

#### Load Images (Добавление изображения в задание)
Вместе с изображением передается его название и uuid задачи к которой необходимо привязать изобржаение. Изображение учитыватеся в статистике в запросе "Получение задания" сразу после завершения запроса.

**Endpoint**: `POST /load_images`

**CURL**:
```
curl -X POST http://127.0.0.1:8000/tevian_test/load_images \
     -H "Authorization: Basic YWxla3NhbmQ6Y29kZXIxMTcw" \
     -F "files=@/path/to/image1.jpg" \
     -F "files=@/path/to/image2.jpg" \
     -F 'data_image={"name": "Image Name", "task_id": "123e4567-e89b-12d3-a456-426614174000"}'
```

**Example Response**:

```json
{
  "info ": "info ": "The image has been processed and added to the task"
}
```

#### Delete Task by ID (Удаление задания)
 При удалении задания все связанные с ним данные будут удалены.

**Endpoint**: `DELETE /delete_task_use_id`

**CURL**:
```
curl -X DELETE http://127.0.0.1:8000/tevian_test/delete_task_use_id \
     -H "Authorization: Basic YWxla3NhbmQ6Y29kZXIxMTcw" \
     -H "Content-Type: application/json" \
     -d '{
           "task_id": "123e4567-e89b-12d3-a456-426614174000"
         }'
```

**Example Response**:

```json
{
   "info ": "Task deleted"
}
```

#### Get Task Details (Получение задания)
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

**Endpoint**: `GET /get_task`

**CURL**:
```
curl -X GET "http://127.0.0.1:8000/tevian_test/get_task?task_id=123e4567-e89b-12d3-a456-426614174000" \
     -H "Authorization: Basic YWxla3NhbmQ6Y29kZXIxMTcw"
```

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