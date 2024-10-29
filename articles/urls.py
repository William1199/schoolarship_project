from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug:slug>", views.detail, name="detail"),
    path("create/article", views.create_article, name="create-article"),
]