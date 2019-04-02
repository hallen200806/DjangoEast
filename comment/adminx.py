import xadmin
from .models import *

class CommentAdmin(object):
    list_display = ['id','object_id','text','comment_time','user']

xadmin.site.register(Comment,CommentAdmin)
