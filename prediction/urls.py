from django.urls import path, include
from . import views
urlpatterns = [

    path('',views.homepage, name='homepage'),
    path('predict/', views.callEvaluate, name='predict'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('news', views.news, name='news'),
   # path('report_activity', views.report_activity, name="report_activity"),
    path('profile', views.profile, name='profile'),
    


]