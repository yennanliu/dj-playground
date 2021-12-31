from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.shortcuts import render_to_response
from django.views.generic.base import View, TemplateView

from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm

#from restaurants.models import Restaurant, Food
#from django.template.loader import get_template

def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        auth.login(request, user)
        return HttpResponseRedirect('/index/')

    else:
        #return render_to_response('registration/login.html',RequestContext(request, locals()))
        return render_to_response('login.html',RequestContext(request, locals()))

# def index(request):
#     return render_to_response('index.html', RequestContext(request, locals()))


class IndexView(TemplateView):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['request'] = request
        return self.render_to_response(context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def welcome(request):
    # if already submit request
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('welcome !!!' + request.GET['user_name'])
    # if not yet submit request
    else:
        return render_to_response('welcome.html', locals())

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')

        else:
            form = UserCreationForm()

    return render_to_response('register.html', RequestContext(request, locals()))


# def here(request):
#     return HttpResponse("helloooo! i am here !!")

class HereView(View):

    def get(self, request):
        return HttpResponse("helloooo! i am here !!")

def add(request, a, b):
    a = int(a)
    b = int(b)
    s = a + b 
    d = a - b
    p = a * b
    q = a / b
    return render_to_response(
        'math.html',
        {'s': s, 'd' : d, 'p': p, 'q': q}
    )
    #t = get_template('math.html')
    #t = template.Template('<html>sum= {{s}}<br>dif = {{d}}<br>pro={{p}} <br> quo = {{q}} </html>')
    #c = template.Context({'s': s, 'd' : d, 'p': p, 'q': q})
    #return HttpResponse(t.render(c))
    # s = int(a) + int(b)
    # return HttpResponse(str(s))
    
# def menu(request):
#     food1 = {'name': 'hamburger',
#             'price' : 199,
#             'comment' : 'great!',
#             'is_spicy' : False
#     }
#     food2 = {'name': 'fries',
#             'price' : 30,
#             'comment' : 'yummy!',
#             'is_spicy' : True
#     }
#     food3 = {'name': 'steak',
#             'price' : 500,
#             'comment' : 'awesome !!!!',
#             'is_spicy' : False
#     }
#     # django will pass foods to menu.html, and for loop all food via jinja syntax
#     foods = [food1, food2, food3]  
#     # locals() will return all local vars in this method
#     return render_to_response('menu.html', locals())


# def menu(request):
#     restaurants = Restaurant.objects.all()
#     return render_to_response("menu.html", locals())
