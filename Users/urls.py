from django.urls import path
from . import views
urlpatterns=[ 
    path("google/", views.GoogleLogin, name='google-login' )
]