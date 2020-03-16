from django.urls import path
from .views import Hits, HitDetail
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('hits/', login_required(Hits.as_view()), name='hits_url'),
    path('hit/<int:id>', login_required(HitDetail.as_view()), name='hit_detail_url')
]
