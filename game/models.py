from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Game(models.Model):
    board = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    created_date = models.DateTimeField(auto_now_add=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.CharField(max_length=1)
    squares = models.CharField(max_length=11)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user}, { 'Finished game' if self.finished_date  else 'Unfinished game'}"
