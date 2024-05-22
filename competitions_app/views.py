from typing import Any

from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .forms import AddFundsForm, Registration
from .models import Competition, Sport, Stage, Client, CompetitionsSports
from .serializers import (CompetitionSerializer, SportSerializer,
                          StageSerializer, CompetitionsSportsSerializer)


def home_page(request):
    return render(
        request,
        'index.html',
        {
            'competitions': Competition.objects.count(),
            'sports': Sport.objects.count(),
            'stages': Stage.objects.count(),
        }
    )

def create_list_view(model_class, plural_name, template):
    class CustomListView(ListView):
        model = model_class
        template_name = template
        paginate_by = 10
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            books = model_class.objects.all()
            paginator = Paginator(books, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return CustomListView

competition_list_view = create_list_view(Competition, 'competitions', 'catalog/competitions.html')
sport_list_view = create_list_view(Sport, 'sports', 'catalog/sports.html')
stage_list_view = create_list_view(Stage, 'stages', 'catalog/stages.html')


def create_view(model_class, context_name, template):
    def view(request):
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        context = {context_name: target}
        if model_class == Sport:
            client = Client.objects.get(user=request.user)
            context['client_subscribed_to_sport'] = target in client.sports.all()
        return render(
            request,
            template,
            context,
        )
    return view

competition_view = create_view(Competition, 'competition', 'entities/competition.html')
sport_view = create_view(Sport, 'sport', 'entities/sport.html')
stage_view = create_view(Stage, 'stage', 'entities/stage.html')


def register(request):
    errors = ''
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
        else:
            errors = form.errors
    else:
        form = Registration()

    return render(
        request,
        'registration/register.html',
        {
            'form': form,
            'errors': errors,
        }
    )

class MyPermission(BasePermission):
    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = 'POST', 'PUT', 'DELETE'

    def has_permission(self, request, _):
        if request.method in self._safe_methods and (request.user and request.user.is_authenticated):
            return True
        if request.method in self._unsafe_methods and (request.user and request.user.is_superuser):
            return True
        return False
        
def create_viewset(model_class, serializer):
    class CustomViewSet(ModelViewSet):
        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return CustomViewSet

competition_viewset = create_viewset(Competition, CompetitionSerializer)
sport_viewset = create_viewset(Sport, SportSerializer)
stage_viewset = create_viewset(Stage, StageSerializer)
competitionssports_viewset = create_viewset(CompetitionsSports, CompetitionsSportsSerializer)


def profile(request):
    client = Client.objects.get(user=request.user)
    form_errors = ''
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount', None)
            if amount:
                client.money += amount
                client.save()
            else:
                form_errors = 'An error occured, money amount was not specified!'
    else:
        form = AddFundsForm()
    
    client_attrs = 'username', 'first_name', 'last_name', 'money'
    client_data = {attr: getattr(client, attr) for attr in client_attrs}
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
            'form': form,
            'form_errors': form_errors,
            'client_books': client.books.all(),
        }
    )
