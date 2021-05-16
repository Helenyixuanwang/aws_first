from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create),
    path('user/dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),

    path('trips/<int:trip_id>', views.display_trip),
    path('trips/<int:trip_id>/delete', views.delete_trip),
    path('trips/new', views.new),
    path('trips/<int:trip_id>/edit', views.edit_trip),
    path('trips/<int:trip_id>/update', views.update_trip),
    path('trips/create',views.create_trip),
    path('trips/<int:trip_id>/join', views.join),
    path('trips/<int:trip_id>/cancel', views.cancel)
    
]