# Social-network

## Init
```bash
# 1) set up env
conda create -n social python=3.8 # python 3.8

# 2) activate env
source activate social

# 3) install django 3.0.5
pip install django==3.0.5

# 4) init django project
django-admin startproject mybffbook

# 5) rename path
cd dj-playground/social-network
mv mybffbook src

# (social) yennanliu@MacBook-Pro social-network % pwd
# /Users/yennanliu/dj-playground/social-network
# (social) yennanliu@MacBook-Pro social-network % ls
# README.md doc       src
# (social) yennanliu@MacBook-Pro social-network % ls src
# manage.py mybffbook

# 6) migrate db
cd dj-playground/social-network/src
python manage.py migrate

# 7) create super user
python manage.py createsuperuser
# account : admin, pwd : 0000

# 8) run
python manage.py runserver

# 9) update collectstatic (### after updating urls.py, settings.py)
python manage.py collectstatic

# (social) yennanliu@MacBook-Pro src % python manage.py collectstatic
# 130 static files copied to '/Users/yennanliu/dj-playground/social-network/static_cdn/static_root'.
```

### Endpoint
- http://127.0.0.1:8000/

## Ref
- https://www.youtube.com/watch?v=ozr6NEomLQw&list=PLgjw1dR712joFJvX_WKIuglbR1SNCeno1&index=1
- https://github.com/hellopyplane/Social-Network