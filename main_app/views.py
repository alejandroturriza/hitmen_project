from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .models import Hit
from account.models import Hitman
from django.db.models import Q
from .forms import HitForm
from django.contrib import messages
from django.contrib.auth.models import User


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
        is_close_case = hit.status in (2, 3)
        if not request.user.has_perm('main_app.change_hit') or is_close_case:
            form.fields['title'].widget.attrs['readonly'] = 'readonly'
            form.fields['assignee'].disabled = True
            form.fields['description'].widget.attrs['readonly'] = 'readonly'
            if is_close_case:
                form.fields['status'].disabled = True
        form.fields['assigned_by'].disabled = True
        users = get_users_fill_select_assignee(request.user)
        form.fields['assignee'].choices = users
        return render(request, 'hit_detail.html', context={'form': form, 'only_view': is_close_case})

    def post(self, request, id):
        hit = get_object_or_404(Hit, pk=id)
        form = HitForm(request.POST, instance=hit)
        if form.is_valid():
            assignee = form.cleaned_data['assignee']
            save_hit = form.save()
            if assignee and save_hit.status is None and save_hit.assigned_by is None:
                save_hit.assigned_by = request.user
                save_hit.status = 1
                save_hit.save()
            messages.success(request, 'Hit update successfuly')
        else:
            messages.error(request, 'hit not update')
        return redirect('hit_detail_url', id=id)


def add_hit(request):
    if request.method == 'POST':
        form = HitForm(request.POST)
        if form.is_valid():
            new_hit = form.save()
            assignee = form.cleaned_data['assignee']
            if assignee and new_hit.status is None and new_hit.assigned_by is None:
                new_hit.assigned_by = request.user
                new_hit.status = 1
                new_hit.save()
            messages.success(request, 'Hit created successfuly')
            form = HitForm()
    else:
        form = HitForm()
    users = get_users_fill_select_assignee(request.user)
    form.fields['assignee'].choices = users
    return render(request, 'hit_detail.html', context={'form': form})


def get_users_fill_select_assignee(user_manager):
    if user_manager.is_superuser:
        users = User.objects.all().exclude(id=user_manager.id)
    elif user_manager.is_staff:
        users = User.objects.filter(
            id__in=Hitman.objects.select_related('manager').filter(manager=user_manager.id).values('user'))
    else:
        users = User.objects.filter(id=user_manager.id)

    return users
