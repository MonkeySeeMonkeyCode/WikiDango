from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    # path("new/<str:page>/", views.new, name="edits"),
    # path("edit/<str:entry>/", views.edit, name="edit"),
    re_path(r'edit/(?P<entry>[\w\ ]+)', views.edit, name="edit"),
    path('random', views.random, name='random'),
    path("<str:title>", views.article, name="article"),
]
