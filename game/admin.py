from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "board",
        "created_date",
        "finished_date",
        "winner",
        "squares",
        "user",
    )
    list_filter = ("created_date",)


admin.site.register(Game, GameAdmin)
