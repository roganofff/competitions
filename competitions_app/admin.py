from django.contrib import admin

from .models import Competition, CompetitionsSports, Sport, Stage, Client, SportClient


class StageInline(admin.TabularInline):
    model = Stage
    extra = 1

class CompetitionsSportsInline(admin.TabularInline):
    model = CompetitionsSports
    extra = 1

class SportClientInline(admin.TabularInline):
    model = SportClient
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (SportClientInline,)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    model = Competition
    inlines = (CompetitionsSportsInline,)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    model = Sport
    inlines = (CompetitionsSportsInline,)

@admin.register(CompetitionsSports)
class CompetitionsSportsAdmin(admin.ModelAdmin):
    model = CompetitionsSports
    inlines = (StageInline,)

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    model = Stage
