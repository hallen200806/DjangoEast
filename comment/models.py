from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import django.utils.timezone as timezone

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,verbose_name="评论来源")
    object_id = models.PositiveIntegerField(verbose_name="评论对象")
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name="评论内容")
    comment_time = models.DateTimeField(verbose_name="评论时间",default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name="评论用户")

    class Meta:
        verbose_name = "我的评论"
        verbose_name_plural = verbose_name