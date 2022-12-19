from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Category(models.Model):
    name=models.CharField(max_length=256)
    slug=models.SlugField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name=models.CharField(max_length=256)
    slug=models.SlugField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name=models.CharField(max_length=256)
    year=models.IntegerField()
    description=models.TextField(null=True)
    genre =models.ManyToManyField(Genre,through='TitleGenre')
    category =models.ForeignKey(Category,null=True,on_delete=models.SET_NULL,related_name='categories')

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    title=models.ForeignKey(Title,on_delete=models.CASCADE,related_name='titles')
    genre=models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genres')

    def __str__(self) -> str:
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title=models.ForeignKey(Title,on_delete=models.CASCADE,related_name='reviews')
    text=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    score=models.PositiveSmallIntegerField()
    pub_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=['title','author']

    
    def __str__(self) -> str:
        return self.text[:15]

class Comment(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='comments')
    text=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    pub_date=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.text[:15]







