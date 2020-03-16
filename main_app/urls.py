from django.urls import path
from .views import Hits, HitDetail, add_hit
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404

urlpatterns = [
    path('hits/', login_required(Hits.as_view()), name='hits_url'),
    path('hit/', login_required(add_hit), name='hit_add_url'),
    path('hit/<int:id>', login_required(HitDetail.as_view()), name='hit_detail_url')
]
