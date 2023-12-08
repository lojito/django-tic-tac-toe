from datetime import datetime
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import GameForm
from .models import Game
from .tictactoe.board import Board
from .tictactoe.computer import Computer
from .tictactoe.constants import (
    COMPUTER,
    NO_PLAYER_YET,
    SQUARE_NOT_FOUND,
    SQUARES_NUMBER,
    USER,
    WINNING_SQUARES_NUMBER,
    RESULT,
    MESSAGES,
)
from .tictactoe.exceptions import (
    BoardInvalidError,
    BoardInvalidPlayerError,
    BoardSquareError,
)


def add_constants_to_context(context):
    context["NO_PLAYER_YET"] = NO_PLAYER_YET
    context["USER"] = USER
    context["COMPUTER"] = COMPUTER
    context["SQUARES_NUMBER"] = SQUARES_NUMBER
    context["WINNING_SQUARES_NUMBER"] = WINNING_SQUARES_NUMBER
    context["MESSAGE_LOST"] = RESULT[COMPUTER]
    context["MESSAGE_WON"] = RESULT[USER]
    context["MESSAGE_TIE"] = RESULT[NO_PLAYER_YET]
    return context


@login_required
def new_game(request):
    game = Game.objects.create(board=NO_PLAYER_YET * SQUARES_NUMBER, user=request.user)
    context = {
        "game": game,
    }
    context = add_constants_to_context(context)
    template = "game/new_game.html"
    return render(request, template, context)


class GameUnfinishedListView(LoginRequiredMixin, ListView):
    template_name = "game/unfinished_games.html"
    model = Game
    context_object_name = "games"

    def get_queryset(self) -> QuerySet[Any]:
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user, finished_date__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["finished"] = False
        return context


class GameUnfinishedView(LoginRequiredMixin, DetailView):
    template_name = "game/game_unfinished.html"
    model = Game

    def get_queryset(self) -> QuerySet[Any]:
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_constants_to_context(context)
        return context

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            obj = Game(board="", id=self.kwargs.get(self.pk_url_kwarg))
        return obj


class GameFinishedListView(LoginRequiredMixin, ListView):
    template_name = "game/finished_games.html"
    model = Game
    context_object_name = "games"

    def get_queryset(self) -> QuerySet[Any]:
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user, finished_date__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites_games = self.request.session.get("favorites_games")
        context["favorite_list"] = [] if favorites_games is None else favorites_games
        context["finished"] = True
        context = add_constants_to_context(context)
        return context


class GameFinishedView(LoginRequiredMixin, DetailView):
    template_name = "game/game_finished.html"
    model = Game

    def get_queryset(self) -> QuerySet[Any]:
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites_games = self.request.session.get("favorites_games")
        context["is_favorite"] = (
            False
            if favorites_games is None
            else self.get_object().pk in favorites_games
        )
        context["squares"] = context["game"].squares.split(",")
        context = add_constants_to_context(context)
        return context

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            obj = Game(board="", id=self.kwargs.get(self.pk_url_kwarg))
        return obj


class GameFavoriteView(LoginRequiredMixin, View):
    def get(self, request):
        favorites_games = request.session.get("favorites_games")

        context = {}

        if favorites_games is None or len(favorites_games) == 0:
            context["games"] = []
        else:
            context["games"] = Game.objects.filter(
                id__in=favorites_games, user=self.request.user
            )
            context = add_constants_to_context(context)

        return render(request, "game/favorites_games.html", context)

    def post(self, request):
        favorites_games = request.session.get("favorites_games")
        if favorites_games is None:
            favorites_games = []
        game_id = int(request.POST["gameid"])
        is_favorite = "True"
        if game_id not in favorites_games:
            favorites_games.append(game_id)
        else:
            favorites_games.remove(game_id)
            is_favorite = "False"

        request.session["favorites_games"] = favorites_games

        return JsonResponse({"isFavorite": is_favorite})


def update_game(request, game_id, finished_game):
    game = get_object_or_404(Game, pk=game_id, user=request.user)
    form = GameForm(request.POST, instance=game)
    if form.is_valid():
        game = form.save(commit=False)
        game.user = request.user
        if finished_game:
            game.finished_date = datetime.now()
            game.winner = request.POST["winner"]
            game.squares = request.POST["squares"]
        game.board = request.board
        game.save()
        return True
    return False


@login_required
def play_game(request):
    try:
        game_id = request.POST["gameid"]
        board = Board(request.POST["board"])
        computer = Computer(board)
        square = computer.play()
        if square == SQUARE_NOT_FOUND:
            return JsonResponse({"error": MESSAGES["BOARD_IS_FULL"]})
        else:
            request.board = str(board)
            if update_game(request, game_id, finished_game=False) is False:
                return JsonResponse(
                    {
                        "squareComputer": square,
                        "error": MESSAGES["INVALID_BOARD"].format(
                            str(board), SQUARES_NUMBER, NO_PLAYER_YET, USER, COMPUTER
                        ),
                    }
                )
            else:
                return JsonResponse({"squareComputer": square, "error": ""})
    except (BoardSquareError, BoardInvalidError, BoardInvalidPlayerError) as e:
        return JsonResponse({"error": str(e)})


@login_required
def won_game(request):
    try:
        board = Board(request.POST["board"])
        result = board.won(request.POST["player"])
        return JsonResponse(
            {"won": str(result[0]), "winningSquares": str(result[1]), "error": ""}
        )

    except BoardInvalidError as e:
        return JsonResponse({"error": str(e)})


@login_required
def save_game(request):
    try:
        game_id = request.POST["gameid"]
        request.board = request.POST["board"]
        if update_game(request, game_id, finished_game=True) is False:
            return JsonResponse(
                {
                    "error": MESSAGES["INVALID_BOARD"].format(
                        request.board, SQUARES_NUMBER, NO_PLAYER_YET, USER, COMPUTER
                    )
                }
            )
        else:
            return JsonResponse({"error": ""})
    except ValueError:
        return JsonResponse({"error": str(ValueError)})


@login_required
def delete_game(request):
    game_id = request.POST["gameid"]
    try:
        game = get_object_or_404(Game, pk=game_id, user=request.user)
        game.delete()
        favorites_games = request.session.get("favorites_games")
        if favorites_games is not None and game_id in favorites_games:
            favorites_games.remove(game_id)
            request.session["favorites_games"] = favorites_games

        if game.finished_date:
            return redirect("game:finished_games")
        else:
            return redirect("game:unfinished_games")
    except Http404:
        return redirect("game:finished_games")
