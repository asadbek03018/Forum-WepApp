
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=320)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums', on_delete=models.CASCADE)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    forum_question = models.CharField(max_length=300)
    forum_slug = models.SlugField(null=False, unique=True)
    forum_image = models.ImageField(upload_to='forums/forum/image/', null=True, blank=True)
    forum_about = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.forum_question

    def save(self, *args, **kwargs):
        if not self.forum_slug:
            self.forum_slug = slugify(self.forum_question)
        return super().save(*args, **kwargs)


class Thread(models.Model):
    forum = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author} on {self.thread.title}"