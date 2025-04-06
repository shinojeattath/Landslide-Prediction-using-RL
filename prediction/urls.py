from django.urls import path, include
from . import views
urlpatterns = [

    path('',views.homepage, name='homepage'),
    path('predict/', views.callEvaluate, name='predict'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('news', views.news, name='news'),
   # path('report_activity', views.report_activity, name="report_activity"),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('prediction_analysis', views.prediction_analysis, name='prediction_analysis'),
    path('api/sensor-data/', views.get_latest_sensor_data, name='sensor_data'),
    path('profile', views.profile, name='profile'),
    


]