from django.urls import path

from . import views


app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.open_entry, name="entry_name"),
    path("CreateNewPage", views.create_new_page, name="CreateNewPage"),
    path("wiki/<str:entry_name>/edit", views.edit_entry, name="edit_entry"),
    path("wiki/<str:entry_name>/delete", views.delete_entry, name="delete_entry"),
    path("random", views.random_entry, name="random")
]
