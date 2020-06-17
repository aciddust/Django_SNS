import os
import uuid

from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import User
from django.core.validators import MaxLengthValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Content(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    likes = models.ManyToManyField(User, related_name='likes')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "컨텐츠"

    def total_likes(self):
        print(self.likes.count(), 'this is count')
        return 0

class Comment(BaseModel):
    # id = models.AutoField(primary_key=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, related_name='comments') # 관계
    comment = models.TextField(validators=[MaxLengthValidator(150)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta():
        ordering = ['id'] # 역순
    
    def __str__(self):
        return str(self.comment)[:30]

# class Like(BaseModel):
#     # id = models.AutoField(primary_key=True)
#     content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, related_name='likes')
#     like = models.BooleanField(default=False)
#     #user = models.ManyToOneField(User, related_name='requirement_comment_likes')
#     user = models.ManyToOneRel(User, related_name='requirement_comment_likes')

#     def __str__(self):
#         return str(self.like)


def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))
    #16자리 고유한 아이디 생성


class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() # image numbering

    class Meta:
        unique_together = ['content', 'order']
        ordering = ['order']


class FollowRelation(BaseModel):
    # follower = models.OneToOneField(User, on_delete=models.CASCADE)
    # followee = models.ManyToManyField(User, related_name='followee')
    follower = models.OneToOneField(User, on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='followee')
