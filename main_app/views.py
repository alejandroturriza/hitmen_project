from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .models import Hit
from account.models import Hitman
from django.db.models import Q
from .forms import HitForm, HitmenForm
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
            hits = Hit.objects.filter(Q(assignee__in=get_hitmans) | Q(assignee=None) | Q(assignee=request.user))
        elif request.user.is_superuser:
            hits = Hit.objects.all()
        return render(request, 'hits.html', context={'hits': hits})


class HitDetail(views.View):
    def get(self, request, id):
        hit = get_object_or_404(Hit, id=id)
        form = HitForm(instance=hit)
        is_close_case = True if hit.status in (2, 3) or (hit.assignee and not hit.assignee.is_active) else False
        if not request.user.has_perm('main_app.change_hit') or is_close_case:
            form.fields['title'].widget.attrs['readonly'] = 'readonly'
            form.fields['assignee'].disabled = True
            form.fields['description'].widget.attrs['readonly'] = 'readonly'
            if is_close_case:
                form.fields['status'].disabled = True
        if not hit.assignee:
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
            if assignee and save_hit.status is None:
                save_hit.assigned_by = request.user
                save_hit.status = 1
                save_hit.save()
            messages.success(request, 'Hit update successfuly')
        else:
            messages.error(request, 'Hit not update', extra_tags='danger')
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
            return redirect('hit_detail_url', id=new_hit.id)
    else:
        form = HitForm()
        form.fields['status'].disabled = True
    users = get_users_fill_select_assignee(request.user)
    form.fields['assignee'].choices = users
    return render(request, 'hit_detail.html', context={'form': form})


def get_users_fill_select_assignee(user_manager):
    if user_manager.is_superuser:
        users = User.objects.all().exclude(id=user_manager.id)
    elif user_manager.is_staff:
        users = User.objects.filter(Q(
            id__in=Hitman.objects.select_related('manager').filter(manager=user_manager.id).values('user')) | Q(
            id=user_manager.id))
    else:
        users = User.objects.filter(id=user_manager.id)

    return users


def get_related_users(manager):
    hitmen = []
    if manager.is_staff and not manager.is_superuser:
        hitmen = Hitman.objects.select_related('manager').filter(manager=manager)
    elif manager.is_superuser:
        hitmen = Hitman.objects.select_related('manager').all()
    return hitmen


def hitmen_list(request):
    hitmen = get_related_users(request.user)
    return render(request, 'hitmen.html', context={'hitmen': hitmen})


class HitmenDetail(views.View):
    def get(self, request, id):
        hitman = Hitman.objects.get(id=id)
        form = HitmenForm(initial={
            'first_name': hitman.user.first_name,
            'last_name': hitman.user.last_name,
            'email': hitman.user.username,
            'description': hitman.description,
            'status': 1 if hitman.user.is_active else 0,
            'manager': hitman.manager
        })
        if not hitman.user.is_active:
            form.fields['first_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['last_name'].widget.attrs['readonly'] = 'readonly'
            form.fields['email'].widget.attrs['readonly'] = 'readonly'
            form.fields['description'].widget.attrs['readonly'] = 'readonly'
            form.fields['status'].disabled = True
            form.fields['manager'].disabled = True
        # get related users
        if request.user.is_staff and not request.user.is_superuser:
            managers = [request.user]
        else:
            managers = User.objects.filter(is_staff=True).exclude(is_superuser=True)
        form.fields['manager'].choices = managers
        return render(request, 'hitmen_detail.html', context={'form': form})

    def post(self, request, id):
        hitman = get_object_or_404(Hitman, pk=id)
        form = HitmenForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            manager = form.cleaned_data['manager']
            if not User.objects.filter(username__iexact=email).exclude(id=hitman.user.id):
                hitman.user.first_name = first_name
                hitman.user.last_name = last_name
                hitman.user.username = email
                hitman.description = description
                hitman.user.is_active = True if status else False
                hitman.manager_id = manager
                hitman.user.save()
                hitman.save()
                messages.success(request, 'Hitmen update successfuly')
            else:
                messages.error(request, 'Email already exists', extra_tags='danger')
        else:
            messages.error(request, 'Hitmen not update', extra_tags='danger')
        return redirect('hitmen_detail_url', id=id)


class HitsBulk(views.View):
    def get(self, request):
        hits, managers = [], []
        if request.user.is_staff and not request.user.is_superuser:
            get_hitmans = Hitman.objects.filter(manager=request.user).values_list('user')
            hits = Hit.objects.filter(Q(assignee__in=get_hitmans) | Q(assignee=None) | Q(assignee=request.user),
                                      Q(status__isnull=True) | Q(status=1))
            managers = get_users_fill_select_assignee(request.user)
        elif request.user.is_superuser:
            hits = Hit.objects.filter(Q(status__isnull=True) | Q(status=1))
            managers = User.objects.filter(is_active=True).exclude(is_superuser=True)
        return render(request, 'hits_bulk.html', context={'hits': hits, 'managers': managers})

    def post(self, request):
        try:
            data_form = dict(filter(lambda x: x[0] != 'csrfmiddlewaretoken', request.POST.items()))
            for x in data_form:
                hit = Hit.objects.get(id=x)
                hit.assignee_id = int(data_form[x]) if isinstance(data_form[x], str) and data_form[x] != '' else None
                hit.status = 1 if hit.assignee_id is not None else None
                hit.assigned_by = request.user
                hit.save()
            messages.success(request, 'Updated Hits!')
        except:
            messages.error(request, 'Not update Hit', extra_tags='danger')
        return redirect('hits_bulk_url')


# error view
def handler500(request):
    return render(request, 'errors/500.html', status=500)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)
