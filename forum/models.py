
from django.db import models
# from django.contrib.auth.models import User
from accounts.models import Account
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=320)
    slug = models.SlugField(null=True, blank=True,  unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum_view', args=[self.slug])

    def __str__(self):
        return self.name





class Forum(models.Model):
    statuss = (
        ('solved', 'Solved'),
        ('unsolved', 'Unsolved')
    )
    category = models.ForeignKey(Category, related_name='forums', on_delete=models.CASCADE)
    moderator = models.ForeignKey(Account, on_delete=models.CASCADE)
    forum_question = models.CharField(max_length=300)
    forum_slug = models.SlugField(null=True, blank=True,  unique=True)
    forum_image = models.ImageField(upload_to='forums/forum/image/', null=True, blank=True)
    forum_about = models.TextField()
    status = models.CharField(max_length=24, choices=statuss)
    forum_views = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.forum_slug:
            self.forum_slug = slugify(self.forum_question)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.forum_question

    def get_forum_views(self):
        return self.forum_views

    def post_url(self):
        return f"/forum/use/{self.category.slug}/{self.forum_slug}/"

    def get_absolute_url(self):
        return reverse('forum_view', args=[self.forum_slug])




class Thread(models.Model):
    forum = models.ForeignKey(Forum, related_name='threads', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(Account, related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    forum = models.ForeignKey(Forum, related_name='forum_posts', blank=True, null=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='threads_posts', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, related_name='author_posts', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='posts/images/')
    parent_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author}"