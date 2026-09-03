from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(max_length=100)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('display_order', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=('category', 'name'),
                name='unique_subcategory_per_category'
            )
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions'
    )
    question = models.CharField(max_length=300)

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.score}/{self.total_questions}"


class QuizAnswer(models.Model):
    result = models.ForeignKey(
        QuizResult,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.result.user.username} - {self.question.question}"
