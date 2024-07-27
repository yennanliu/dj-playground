# Chat Room App

## Run
```bash
cd chat-room/mysite/

# init migrate
python manage.py migrate

# run app
# (make sure at same level with manage.py)
python3 manage.py runserver
```

```bash
# check DB
sqlite3 db.sqlite3
```

## Endpoints

- http://127.0.0.1:8000/chat/
  - http://127.0.0.1:8000/chat/lobby/

- http://127.0.0.1:8000/admin/

## Ref

- https://github.com/django/channels
- https://channels.readthedocs.io/en/latest/

- tutorial
  - https://channels.readthedocs.io/en/latest/tutorial/index.html
- init setup
  - https://channels.readthedocs.io/en/latest/tutorial/part_1.html
  - https://channels.readthedocs.io/en/latest/tutorial/part_2.html