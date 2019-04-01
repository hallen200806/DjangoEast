import xadmin
from .models import *

class CommentAdmin(object):
    list_display = ['content_object','text','comment_time','user']
    model_icon = 'fa fa-commenting'

xadmin.site.register(Comment,CommentAdmin)
