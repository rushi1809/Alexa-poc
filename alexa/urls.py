from django.urls import path
from .views import alexa_webhook

urlpatterns = [
    path("", alexa_webhook),
]