from django.urls import path
from .views import Hits
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('hits/', login_required(Hits.as_view()), name='hits_url'),
]
