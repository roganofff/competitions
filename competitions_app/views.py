"""Module for page views."""
from typing import Any

from django.contrib.auth import authenticate, decorators, login, logout
from django.core import exceptions
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from competitions_app import config, serializers

from .forms import AddFundsForm, LoginForm, MakeBetForm, Registration
from .models import Client, Competition, CompetitionsSports, Sport, Stage


def home_page(request):
    """Return home page.

    Args:
        request: HTTP request.

    Returns:
        HttpResponse: return an HttpResponse.
    """
    return render(
        request,
        'index.html',
        {
            'competitions': Competition.objects.count(),
            'sports': Sport.objects.count(),
            config.STAGES: Stage.objects.count(),
        },
    )


def create_list_view(model_class, plural_name, template):
    """Create list view pages.

    Args:
        model_class (models): desired model for list view.
        plural_name (str): models name in plural form.
        template (str): path to html template.

    Returns:
        CustomListView: list view.
    """
    class CustomListView(ListView):
        """Custom list view.

        Args:
            ListView: Render some list of objects

        Returns:
            CustomListView: list view.
        """

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
stage_list_view = create_list_view(Stage, config.STAGES, 'catalog/stages.html')


def create_view(model_class, context_name, template):
    """Create view.

    Args:
        model_class: desired model class.
        context_name: working context.
        template: path to http template

    Returns:
        view: HttpResponse
    """
    @decorators.login_required
    def view(request):
        """View response.

        Args:
            request: HTTP request.

        Returns:
            HttpResponse: return an HttpResponse.
        """
        id_ = request.GET.get('id', None)
        target = model_class.objects.get(id=id_) if id_ else None
        context = {context_name: target}
        if model_class == Competition:
            next_targets = Sport.objects.all().filter(competitions=target)
            context['sports'] = next_targets
        elif model_class == Sport:
            comps_sport = CompetitionsSports.objects.all().filter(sport_id=target)
            next_targets = [
                Stage.objects.all().filter(comp_sport=comp_sport) for comp_sport in comps_sport
            ]
            context['query_stages'] = next_targets
        elif model_class == Stage:
            client = Client.objects.get(user=request.user)
            context['client_placed_bet'] = target in client.stages.all()
        return render(
            request,
            template,
            context,
        )
    return view


competition_view = create_view(Competition, 'competition', 'entities/competition.html')
sport_view = create_view(Sport, 'sport', 'entities/sport.html')
stage_view = create_view(Stage, config.STAGE, 'entities/stage.html')


def register(request):
    """Register page.

    Args:
        request: HTTP request.

    Returns:
        HttpResponse: return an HttpResponse.
    """
    errors = ''
    if request.method == config.POST:
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
            config.FORM: form,
            'errors': errors,
        },
    )


def login_view(request):
    """
    View function for handling the login process.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page with the form and error message.
    """
    error_message = None

    if request.method == config.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data
            user = authenticate(
                request,
                username=login_data['username'],
                password=login_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
        else:
            error_message = 'Форма неверно заполнена.'
    else:
        form = LoginForm()

    context = {
        config.FORM: form,
        'error_message': error_message,
    }
    return render(request, 'registration/login.html', context)


@decorators.login_required
def logout_view(request):
    """Logout from your account.

    Args:
        request: request.

    Returns:
        redirect: html page.
    """
    logout(request)
    return render(request, 'registration/logged_out.html', {})


class MyPermission(BasePermission):
    """Custom permission.

    Args:
        BasePermission: a base class from which all permission classes should inherit.

    Returns:
        bool: is user permitted to do this.
    """

    _safe_methods = 'GET', 'HEAD', 'OPTIONS', 'PATCH'
    _unsafe_methods = 'POST', 'PUT', 'DELETE'

    def has_permission(self, request, _):
        """Check if has permission.

        Args:
            request: request.
            _: some statement idk.

        Returns:
            bool: is user permitted to do this.
        """
        user = request.user
        if user and user.is_authenticated:
            if request.method in self._safe_methods:
                return True
            if request.method in self._unsafe_methods and user.is_superuser:
                return True
        return False


def create_viewset(model_class, serializer):
    """Create view set for route.

    Args:
        model_class: desired model class.
        serializer: hyperlink serializer.

    Returns:
        CustomViewSet: view set.
    """
    class CustomViewSet(ModelViewSet):
        """CustomViewSet.

        Args:
            ModelViewSet: model view set.
        """

        serializer_class = serializer
        queryset = model_class.objects.all()
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return CustomViewSet


competition_viewset = create_viewset(Competition, serializers.CompetitionSerializer)
sport_viewset = create_viewset(Sport, serializers.SportSerializer)
stage_viewset = create_viewset(Stage, serializers.StageSerializer)
competitionssports_viewset = create_viewset(
    CompetitionsSports,
    serializers.CompetitionsSportsSerializer,
)


@decorators.login_required
def profile(request):
    """Return profile page.

    Args:
        request: request.

    Returns:
        HttpResponse: html page.
    """
    client = Client.objects.get(user=request.user)
    form_errors = ''
    if request.method == config.POST:
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
    front_attrs = 'Username', 'First name', 'Last name', 'Balance'
    client_data = {
        front_attr: getattr(client, back_attr)
        for (back_attr, front_attr) in zip(client_attrs, front_attrs)
    }
    return render(
        request,
        'pages/profile.html',
        {
            'client_data': client_data,
            config.FORM: form,
            'form_errors': form_errors,
            'client_stages': client.stages.all(),
        },
    )


@decorators.login_required
def make_bet(request):
    """Return page to make a bet.

    Args:
        request: request.

    Returns:
        HttpResponse: html page.
    """
    client = Client.objects.get(user=request.user)
    id_ = request.GET.get('id', None)
    form_error = ''
    if not id_:
        return redirect(config.STAGES)
    try:
        stage = Stage.objects.get(id=id_)
    except (exceptions.ValidationError, exceptions.ObjectDoesNotExist):
        return redirect(config.STAGES)
    if not stage:
        return redirect(config.STAGES)
    if stage in client.stages.all():
        return redirect('profile')

    if request.method == config.POST and client.money >= 100:
        form = MakeBetForm(request.POST)
        if form.is_valid():
            bet_amount = form.cleaned_data.get('bet_amount')
            client.stages.add(stage)
            client.money -= bet_amount
            client.save()
            return redirect('profile')
        else:
            form_error = form.errors
    else:
        form = MakeBetForm()

    return render(
        request,
        'pages/bet.html',
        {
            'money': client.money,
            config.STAGE: stage,
            config.FORM: form,
            'form_error': form_error,
        },
    )
