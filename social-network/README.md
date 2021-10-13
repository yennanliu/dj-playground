# Social-network

## Init
```bash
# set up env
conda create -n social python=3.8 # python 3.8

# activate env
source activate social

# django 3.0.5
pip install django==3.0.5

# init django project
django-admin startproject mybffbook

# rename path
cd dj-playground/social-network
mv mybffbook src

# (social) yennanliu@MacBook-Pro social-network % pwd
# /Users/yennanliu/dj-playground/social-network
# (social) yennanliu@MacBook-Pro social-network % ls
# README.md doc       src
# (social) yennanliu@MacBook-Pro social-network % ls src
# manage.py mybffbook

# migrate db
cd dj-playground/social-network/src
python manage.py migrate
```

## Ref
- https://www.youtube.com/watch?v=ozr6NEomLQw&list=PLgjw1dR712joFJvX_WKIuglbR1SNCeno1&index=1
- https://github.com/hellopyplane/Social-Network

