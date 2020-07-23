from django.urls import path
from  .  import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.main),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('add_fav', views.add_fav),
    path('books/<id>', views.show_book),
    path('edit_book', views.edit_book),
    path('del_book', views.del_book),
    path('unfav', views.unfav),
    path('fav', views.fav),
]