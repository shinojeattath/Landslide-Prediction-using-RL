from django.urls import path, include
from . import views
urlpatterns = [

    path('',views.homepage, name='homepage'),
    path('predict/', views.callEvaluate, name='predict'),
]