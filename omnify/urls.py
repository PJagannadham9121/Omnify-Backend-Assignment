
from django.contrib import admin
from django.urls import path

from fitness.api import api as fitness_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', fitness_api.urls),
]
