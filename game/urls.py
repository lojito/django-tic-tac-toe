from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("new/", views.new_game, name="new_game"),
    path(
        "unfinished_games/",
        views.GameUnfinishedListView.as_view(),
        name="unfinished_games",
    ),
    path(
        "<int:pk>/game_unfinished/",
        views.GameUnfinishedView.as_view(),
        name="game_unfinished",
    ),
    path(
        "finished_games/", views.GameFinishedListView.as_view(), name="finished_games"
    ),
    path(
        "<int:pk>/game_finished/",
        views.GameFinishedView.as_view(),
        name="game_finished",
    ),
    path(
        "favorite/",
        views.GameFavoriteView.as_view(),
        name="favorite_game",
    ),
    path("play/", views.play_game, name="play_game"),
    path("won/", views.won_game, name="won_game"),
    path("save/", views.save_game, name="save_game"),
    path("delete/", views.delete_game, name="delete_game"),
]
