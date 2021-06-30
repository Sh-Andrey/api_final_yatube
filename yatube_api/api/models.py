from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', 
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL,
        related_name='posts', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', 
        auto_now_add=True, 
        db_index=True
    )

    def __str__(self):
        return self.text


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )

    class Meta:
        models.UniqueConstraint(
            fields=('user', 'following'),
            name='following_user',
        )