"""Module for Django admin panel."""
from django.contrib import admin

import competitions_app.models as models


class StageInline(admin.TabularInline):
    """Stage inline for admin panel.

    Args:
        admin (TabularInline): tabular inline.
    """

    model = models.Stage
    extra = 1


class CompetitionsSportsInline(admin.TabularInline):
    """Competitions Sports inline for admin panel.

    Args:
        admin (TabularInline): tabular inline.
    """

    model = models.CompetitionsSports
    extra = 1


class StageClientInline(admin.TabularInline):
    """Stage client inline for admin panel.

    Args:
        admin (TabularInline): tabular inline.
    """

    model = models.StageClient
    extra = 1


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """Client admin panel.

    Args:
        admin (ModelAdmin): Encapsulate all admin options and functionality for a given model.
    """

    model = models.Client
    inlines = (StageClientInline,)


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    """Competition admin panel.

    Args:
        admin (ModelAdmin): Encapsulate all admin options and functionality for a given model.
    """

    model = models.Competition
    inlines = (CompetitionsSportsInline,)


@admin.register(models.Sport)
class SportAdmin(admin.ModelAdmin):
    """Sport admin panel.

    Args:
        admin (ModelAdmin): Encapsulate all admin options and functionality for a given model.
    """

    model = models.Sport
    inlines = (CompetitionsSportsInline,)


@admin.register(models.CompetitionsSports)
class CompetitionsSportsAdmin(admin.ModelAdmin):
    """Competitions Sports admin panel.

    Args:
        admin (ModelAdmin): Encapsulate all admin options and functionality for a given model.
    """

    model = models.CompetitionsSports
    inlines = (StageInline,)


@admin.register(models.Stage)
class StageAdmin(admin.ModelAdmin):
    """Stage admin panel.

    Args:
        admin (ModelAdmin): Encapsulate all admin options and functionality for a given model.
    """

    model = models.Stage
