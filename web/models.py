from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class Game(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class TextBlock(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.identifier

class FeaturesText(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.identifier


class Faq(models.Model):
    # number = models.CharField(max_length=50)
    question = models.CharField(max_length=100)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question

class Image(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.identifier
