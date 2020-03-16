from django.shortcuts import render, HttpResponse, redirect
from django import views, template
from .models import Hit
from account.models import Hitman
from django.db.models import Q
from .forms import HitForm
from django.shortcuts import get_object_or_404
from django.contrib import messages


def redirect_to_hits(request):
    return redirect('/hits/')


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


class HitDetail(views.View):
    def get(self, request, id):
        hit = Hit.objects.get(id=id)
        form = HitForm(instance=hit)
        if not request.user.has_perm('app.change_hit'):
            form.fields['title'].widget.attrs['readonly'] = 'readonly'
            form.fields['assignee'].disabled = True
            form.fields['description'].widget.attrs['readonly'] = 'readonly'
        form.fields['assigned_by'].disabled = True
        return render(request, 'hit_detail.html', context={'form': form})

    def post(self, request, id):
        hit = get_object_or_404(Hit, pk=id)
        form = HitForm(request.POST, instance=hit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hit update successfuly')
        else:
            messages.error(request, 'hit not update')
        return redirect('hit_detail_url', id=id)