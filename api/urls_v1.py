from django.urls import path, include

urlpatterns = [
    path('/users', include('apps.users.urls')),
    path('/restaurants', include('apps.restaurants.urls'))
]