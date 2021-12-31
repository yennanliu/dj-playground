"""
legacy code for views.py
"""

# @login_required
# def list_restaurants(request):
#     restaurants = Restaurant.objects.all()
#
#     print (request.user.user_permissions.all())
#     # try to storage object via session
#     request.session['restaurants'] = restaurants
#     return render_to_response('restaurants_list.html', RequestContext(request, locals()))


# def menu(request):
#     """retrun a menu response
#     :request: client request
#     :returns: http response
#     """
#     if 'id' in request.GET and request.GET['id'] != '':
#         restaurant = Restaurant.objects.get(id=request.GET['id'])
#         return render_to_response('menu.html', locals())
#     else:
#         return HttpResponseRedirect("/restaurants_list/")

# @permission_required('restaurants.can_comment', login_url='/accounts/login/')
# def comment(request, id):
#     if id:
#         r = Restaurant.objects.get(id=id)
#     else:
#         return HttpResponseRedirect("/restaurants_list/")
#     if request.POST:
#         f = CommentForm(request.POST)
#         if f.is_valid():
#             visitor = f.cleaned_data['visitor']
#             content = f.cleaned_data['content']
#             email = f.cleaned_data['email']
#             date_time = timezone.localtime(timezone.now())
#             c = Comment.objects.create(
#                 visitor=visitor,
#                 email=email,
#                 content=content,
#                 date_time=date_time,
#                 restaurant=r
#                 )
#             f = CommentForm()

#     else:
#         f = CommentForm()

#     return render_to_response('comment.html', RequestContext(request, locals())) 

# def menu(request, id):
#     if id:
#         restaurant = Restaurant.objects.get(id=id)
#         return render_to_response("menu.html", locals())
#     else:
#         return HttpResponseRedirect("/restaurants_list/")

# def comment(request, id):
#     errors = []
#     if id:
#         r = Restaurant.objects.get(id=id)
#     else:
#         return HttpResponseRedirect("/restaurants_list/")
#     if request.POST:
#         visitor = request.POST['visitor']
#         content = request.POST['content']
#         email = request.POST['email']
#         date_time = timezone.localtime(timezone.now())

#         # error handling
#         if any(not request.POST[k] for k in request.POST):
#             errors.append('* there is some blank field, plz fill again')

#         if '@' not in email:
#             errors.append('* email format not correct, plz fill again')

#         if not errors:
#             Comment.objects.create(
#                 visitor=visitor,
#                 email=email,
#                 content=content,
#                 date_time=date_time,
#                 restaurant=r
#             )
#             #visitor, email, content = ('', '', '')
#     f = CommentForm()
#     return render_to_response('comment.html', RequestContext(request, locals()))

# def menu(request):
#     path = request.path
#     #restaurants = Restaurant.objects.all()
#     restaurant = Restaurant.objects.get(id=1)
#     print ("restaurant = " + str(restaurant))
#     return render_to_response("menu.html", locals())

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