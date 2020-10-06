from django.db import models

from api.title.models import Title
from api.users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="titles"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviewer"
    )
    score = models.PositiveSmallIntegerField(null=True)
    pub_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_author"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comment"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата комментария",
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
