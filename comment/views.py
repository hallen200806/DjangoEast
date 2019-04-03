from django.shortcuts import render,reverse,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.form import CommentForm
from django.http import JsonResponse

# 添加评论
def update_comment(request):
    referer = request.META.get('HTTP_REFERER',reverse('blog:index')) # HTTP_REFERER是请求头的一部分，告诉服务器是从哪里来的
    comment_form = CommentForm(request.POST, user=request.user)

    data = {}
    if comment_form.is_valid():
        # 检查通过、保存数据
        comment = Comment()
        comment.text = comment_form.cleaned_data['text']
        comment.user = comment_form.cleaned_data['user']
        comment.content_object = comment_form.cleaned_data['content_object']  # 疑点
        comment.save()
        # # 重定向到原来的页面
        # return redirect(referer)

        # 正确、返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] =  comment.text
    else:
        # return render(request,'error.html',{'error_message':comment_form.errors,'redirect_to':referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)