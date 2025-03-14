from django.urls import path
from . import views

app_name='TestYMLScripts'
urlpatterns = [
    path('update-tests/', views.update_tests, name="update_tests"),
    path('save-tests/', views.save_tests, name='save_tests'),
]