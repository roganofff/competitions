from django.contrib import admin

from .models import Competition, CompetitionsSports, Sport, Stage

class StageInline(admin.TabularInline):
    model = Stage
    extra = 1

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    model = Competition
    inlines = (StageInline,)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    model = Sport
    inlines = (StageInline,)

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    model = Stage