from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from mysite.views import *
from restaurants.views import *

#from django.contrib.auth import views as auth_views
# below is django default login logout method (default login, logout uses login.html under mysite/templates/registration)
#from django.contrib.auth.views import login, logout

urlpatterns = patterns(
    '',
    # mysite
    #url(r'^here/$', here),
    url(r'^here/$', HereView.as_view()),
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns(
    # restaurants
    url(r'^(\d{1,2})/plus/(\d{1,2})/$', add),
    #url(r'^menu/$', menu),
    url(r'^menu/(?P<pk>\d+)/$', MenuView.as_view()),
    url(r'^welcome/$', welcome),
    #url(r'^restaurants_list/$', list_restaurants),
    url(r'^restaurants_list/$', login_required(RestaurantView.as_view())),
    #url(r'^comment/(\d{1,5})/$', CommentView),
    url(r'^comment/(?P<pk>\d+)/$', CommentView.as_view()),
    #url(r'^accounts/', include('django.contrib.auth.urls')), # login
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^index/$', IndexView.as_view()),
    url(r'^accounts/register/$', register)
    )
