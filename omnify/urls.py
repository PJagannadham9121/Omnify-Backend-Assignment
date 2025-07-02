
from django.contrib import admin
from django.urls import path
from fitness.api import router as fitness_router


from ninja import NinjaAPI
api = NinjaAPI()
api.add_router("", fitness_router)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
