# Dj-Restaurants

> Build restaurants app via Django framework
- Python 3.4, Django 1.7
- User flow
```
Home page (index) -> Register -> Login -> Restaurants list -> Menu -> Comment
```

### 1) Installation

<details>
<summary>Install</summary>

```bash
# install py 3.4 with conda
# V1
conda create -n django-env python=3.4

# V2  (if your conda can't install python 3.4 by default)
# https://stackoverflow.com/questions/57449169/how-to-install-deprecated-unsupported-python-3-4-on-conda-environment
conda config --set restore_free_channel True
conda create -n django-env python=3.4

# init env
source activate django-env

# install dependency
pip install -r requirements.txt
```
</details>

### 2) Quick Start
```bash
source activate django-env
cd dj-restaurants/mysite
python manage.py runserver
```

### 3) Operation

<details>
<summary>Operation</summary>

### general OP
```bash
# 1) init project
source activate django-env
cd dj-restaurants 
django-admin.py startproject mysite

# 2) init restaurants app
cd dj-restaurants/mysite && python manage.py startapp restaurants

# 3) check if DB model is correct
python manage.py check

# 4) make DB migration
# restaurants
python manage.py makemigrations restaurants
# admin
python manage.py makemigrations admin

# 5) make admin superuser
python manage.py createsuperuser

# 6) after adding "comment" DB model
python manage.py makemigrations restaurants
python manage.py migrate restaurants
```

### DB op (via django shell)
```python
# manually insert test data
python manage.py shell   

# in the django shell
# make restaurants records
from restaurants.models import Restaurant, Food
r1 = Restaurant(name="burger king", phone_number = '123', address = 'some address')
r1.save()
r2 = Restaurant(name="shokiya", phone_number = '456', address = 'some address 2')
r2.save()

restaurants = Restaurant.objects.all()

# make Food records
r = Restaurant.objects.get(name= "burger king")
f1 = Food(name='burger', price = 120, comment='great', is_spicy=True, restaurant=r)
f1.save()

r = Restaurant.objects.get(name= "shokiya")
f2 = Food(name='shushi', price = 500, comment='ohhh', is_spicy=True, restaurant=r)
f2.save()
```

### Form (comment form) OP
```python
from restaurants.forms import CommentForm

f = CommentForm()

print (f)

# output page
f.as_p()

# output list
f.as_ul()

# output table
f.as_table()
```

### Session OP
```python
from django.contrib.sessions.models import Session

# example func
def use_session(request):
    request.session['lucky_number'] = 8 # set up lucky number
    if 'lucky_number' in request.session:
        lucky_number = request.session['lucky_number']
        # read lucky_number
        response = HttpResponse('your lucky number is ' + lucky_number)
    del request.session['lucky_number'] # delete lucky_number
    return response

def session_test1(request):
    sid = request.COOKIES['sessionid']
    s = Session.objects.get(pk=sid)
    s_info = 'Session ID: ' + sid + 'expire_date: ' + str(s.expire_date) + \
    ' data : ' + str(s.get_decoded())
    return HttpResponse(s_info)

def session_test2(request):
    sid = request.session.session_key
    s = Session.objects.get(pk=sid)
    s_info = 'Session ID: ' + sid + 'expire_date: ' + str(s.expire_date) + \
    ' data : ' + str(s.get_decoded())
    return HttpResponse(s_info)

# command
s = Session.objects.all()[0]
s.expire_date
s.session_data
s.get_decoded()
```

### Permission OP
```python
from restaurants.models import Comment
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Comment)

permission = Permission.objects.create(
    codename='can_comment',
    name='Can comment',
    content_type=content_type
    )
```

### Add user with specific permission
```python
from django.contrib.auth.models import User, Permission

# plz make a new user with username = test_user1 first
user = User.objects.get(username='test_user1')
perm = Permission.objects.get(codename='can_comment')
user.has_perm('restaurants.can_comment')

user = User.objects.get(username='test_user1')
user.has_perm('restaurants.can_comment')

user.user_permissions.remove(perm)
user = User.objects.get(username='test_user1')
user.has_perm('restaurants.can_comment')
```

</details>

### 4) Project Structure

<details>
<summary>Structure</summary>

```
├── README.md
├── doc
│   └── progress.md
├── mysite
│   ├── db.sqlite3
│   ├── manage.py
│   ├── mysite
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── restaurants
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   └── templates
│       ├── math.html
│       └── menu.html
└── requirements.txt
```

</details>

### 5) Endpoints
|  Name  | Url | Description |
| --- | ----- | -------- |
| Home page | http://127.0.0.1:8000/index/ |  |
| Register | http://127.0.0.1:8000/accounts/register/ |  |
| Login | http://127.0.0.1:8000/accounts/login/ |  |
| Admin | http://127.0.0.1:8000/admin/ |  (account : admin, pwd : admin) |
| Restaurants list | http://127.0.0.1:8000/restaurants_list/ |  |
| Menu | http://127.0.0.1:8000/menu/?id=1 | http://127.0.0.1:8000/menu/?id=2  ...|
| Comment | http://127.0.0.1:8000/comment/1/ | http://127.0.0.1:8000/comment/2/ ... |

### 6) Ref
- https://github.com/its-django/mysite