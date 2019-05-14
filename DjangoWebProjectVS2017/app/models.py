"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    subject = models.CharField(default='', max_length=200)
    number_responses = models.IntegerField(
        default=2, 
        validators=[MinValueValidator(2), MaxValueValidator(4)]
    )
    correct_answer = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    is_correct_answer = models.BooleanField()
    votes = models.IntegerField(default=0)

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)