from django.shortcuts import render,reverse,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType

# 添加评论
def update_comment(request):
    # 获取评论信息
    user = request.user
    text = request.POST.get('text','')
    content_type = request.POST.get('content_type','')
    object_id = int(request.POST.get('object_id',''))

    # 获取评论对象
    model_class = ContentType.objects.get(model = content_type).model_class() # 获取模型
    model_obj = model_class.objects.get(pk = object_id) # 获取模型下的某个目标

    # 写入评论
    comment = Comment()
    comment.text = text
    comment.user = user
    comment.content_object = model_obj # 疑点
    comment.save()

    # 重定向到原来的页面
    referer = request.META.get('HTTP_REFERER',reverse('blog:index')) # HTTP_REFERER是请求头的一部分，告诉服务器是从哪里来的
    return redirect(referer)
