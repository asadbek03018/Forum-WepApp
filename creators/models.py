from django.db import models
# from django.contrib.auth.models import User
from forum.models import Forum
from accounts.models import Account



class ForumCreators(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, related_name='users', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Creator: {self.user.username} -> Forum {self.forum.forum_question}"

