# Chat Room App

## Run
```bash
cd chat-room/mysite/

# init migrate
python manage.py migrate

# run app
# (make sure at same level with manage.py)
python3 manage.py runserver


# start redis 
brew services start redis

# check
redis-cli ping
```

```bash
# check DB
sqlite3 db.sqlite3
```

## Create user
```bash
#(venv) ➜  chat-room git:(main) ✗ cd mysite 
#(venv) ➜  mysite git:(main) ✗ ls
#chat       db.sqlite3 manage.py  mysite
#(venv) ➜  mysite git:(main) ✗ python manage.py createsuperuser
#Username (leave blank to use 'yennanliu'): admin
#Email address: admin@uber.com
#Password: 
#Password (again): 
#The password is too similar to the username.
#This password is too short. It must contain at least 8 characters.
#This password is too common.
#Bypass password validation and create user anyway? [y/N]: y
#Superuser created successfully.
```

## Endpoints

- http://127.0.0.1:8000/chat/
  - http://127.0.0.1:8000/chat/lobby/

- http://127.0.0.1:8000/admin/
  - user, pwd : `admin`


## Concept

- channel : A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.
- group : A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.

## Ref

- https://github.com/django/channels
- https://channels.readthedocs.io/en/latest/

- tutorial
  - https://channels.readthedocs.io/en/latest/tutorial/index.html
- init setup
  - https://channels.readthedocs.io/en/latest/tutorial/part_1.html
  - https://channels.readthedocs.io/en/latest/tutorial/part_2.html