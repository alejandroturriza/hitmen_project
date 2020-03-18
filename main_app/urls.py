from django.urls import path
from .views import Hits, HitDetail, add_hit, hitmen_list, HitmenDetail, HitsBulk
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('hits/', login_required(Hits.as_view()), name='hits_url'),
    path('hits/bulk/', login_required(HitsBulk.as_view()), name='hits_bulk_url'),
    path('hit/', login_required(add_hit), name='hit_add_url'),
    path('hit/<int:id>', login_required(HitDetail.as_view()), name='hit_detail_url'),
    path('hitmen/', login_required(hitmen_list), name='hitmen_url'),
    path('hitmen/<int:id>/', login_required(HitmenDetail.as_view()), name='hitmen_detail_url'),
]
