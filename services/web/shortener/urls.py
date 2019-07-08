from django.urls import path, re_path
from .views import IndexView, redirect_view, shorten_view

app_name = 'shortener'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^(?P<subpart_inner>\w{6})$',
            redirect_view, name='redirect'),
    path('shorten/', shorten_view, name='shorten'),
]
