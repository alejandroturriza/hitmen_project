from django.shortcuts import render, HttpResponse, redirect
from django import views
from .models import Hit
from account.models import Hitman
from django.db.models import Q


class Hits(views.View):
    def get(self, request):
        hits = []
        if not request.user.is_staff and not request.user.is_superuser and request.user.hitman_user:
            hits = Hit.objects.filter(assignee=request.user)
        elif request.user.is_staff and not request.user.is_superuser:
            get_hitmans = Hitman.objects.filter(manager=request.user).values_list('user')
            hits = Hit.objects.filter(Q(assignee__in=get_hitmans) | Q(assignee=None))
        elif request.user.is_superuser:
            hits = Hit.objects.all()

        return render(request, 'hits.html', context={'hits': hits})


def redirect_to_hits(request):
    return redirect('/hits/')
