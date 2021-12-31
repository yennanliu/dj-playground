from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import template
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from restaurants.permissions import user_can_comment

from django.utils.decorators import method_decorator
from django.utils import timezone

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView

from restaurants.models import Restaurant, Food, Comment
from restaurants.forms import CommentForm


class MenuView(DetailView):

    model = Restaurant
    template_name = 'menu.html'
    context_object_name = 'restaurant'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuView, self).dispatch(request, *args, **kwargs)

    # overwrite get method
    def get(self, request, pk, *args, **kwargs):
        try:
            return super(MenuView, self).get(self, request, pk=pk, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/restaurants_list/')

class RestaurantView(ListView):

    model = Restaurant
    template_name = 'restaurants_list.html'
    context_object_name = "restaurants"

class CommentView(FormView, SingleObjectMixin):

    """View associated with form"""

    form_class = CommentForm
    template_name = 'comment.html'
    success_url = '/comment/'
    initial = {'content': u'I have no idea'}
    model = Restaurant
    context_object_name = 'r'

    def form_valid(self, form):
        """form is validated, so use form data to create comment
        :form: validated form
        :returns: origin form_valid
        """
        Comment.objects.create(
            visitor=form.cleaned_data['visitor'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=self.get_object()
        )
        return self.render_to_response(self.get_context_data(
                form=self.form_class(initial=self.initial))
        )

    def get_context_data(self, **kwargs):
        """ assign attribute "object" that indicates the query object
        :returns: origin context get from get_context_data with additional object parameter
        """
        self.object = self.get_object()
        return super(CommentView, self).get_context_data(object=self.object, **kwargs)

    @method_decorator(user_passes_test(user_can_comment, login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        """ return decorated dispatch
        :request: request
        :returns: return origin dispatch
        """
        return super(CommentView, self).dispatch(request, *args, **kwargs)
