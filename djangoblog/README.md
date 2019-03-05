##后台文章页使用富文本编辑器Ueditor的方式

1. 安装DjangoUeditor3-master

2. settings.py中注册DjangoUeditor  

3. 项目的url.py文件中注册url

4. model.py中对Post的body字段设置

5. xadmin的plugins中添加ueditor.py文件

6. adminx.py文件中的PostAdmin类中添加一个style_fields变量

##后台文章页使用Markdown编辑器的方式

1. 在Django项目环境中pip安装Markdown包

2. view.py文件中引入Markdown

3. view.py中的article函数中使用Markdown函数进行渲染

4. 后台添加文章时在body中直接放入Markdown格式的源码

5. article模板页关闭autoeascpe功能

6. 首页打开文章就可以看到渲染后的Markdown格式的文章

##Markdown支持代码高亮

1. pip安装pygments

2. 下载高亮代码样式：https://github.com/zmrenwu/django-blog-tutorial/tree/master/blog/static/blog/css/highlights

3. 将你喜欢的代码样式.css文件放入static的css文件夹内

4. 在base.html中引入该样式

5. 后台文章页用``` python ```来引用样式

##Django Haystack实现功能丰富的全文检索

1. pip安装 whoosh(搜索引擎) django-haystack(搜索框架) jieba(中文分词)三件套
```markdown
    whoosh:搜索引擎，进行建立索引、进行分词的功能实现
    haystack：搜索引擎框架，是用户与搜索引擎whoosh的沟通桥梁，负责与搜索引擎进行对接
    jieba：搜索引擎whoosh只能进行英文的分词，jieba是一款中文分词软件
```
2. 注册haystack到设置中的Django APP中

3. 加入下面的配置代码，配置搜索引擎和搜索框架haystack
```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#指定如何对搜索结果分页，这里设置为每 10 项结果为一页  
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
#当添加、修改、删除数据时，自动生成最新索引【注意是通过访问django修改时，直接在数据库中修改不会，因为这是django中配置的】
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

4. blog目录下新建一个search_indexes.py，告诉 django haystack 使用那些数据建立索引以及如何存放索引
```python
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
```

5. 按下列目录创建文件templates/search/indexes/youapp/\<model_name>_text.txt，并添加内容
```python
{{ object.title }}
{{ object.body }}
```
6. 配置在项目目录下的url.py设置URL
```python
urlpatterns = [
    # 其它...
    url(r'^search/', include('haystack.urls')),
]
```

7. 在模板中添加搜索框，并将搜索的内容提交给搜索引擎，通过action
```html
<form role="search" method="get" id="searchform" action="{% url 'haystack_search' %}">
  <input type="search" name="q" placeholder="搜索" required>
  <button type="submit"><span class="ion-ios-search-strong"></span></button>
</form>
```

8. 在templates/search/目录下创建搜索结果页面search.html
```html
传递的结果是一个page变量，可以对他进行循环，然后分页。 
{% for result in page.object_list %}
    要取得 Post（文章）以显示文章的数据如标题、正文，需要从 result 的 object 属性中获取
    {{ result.pbject.title}}
    
    query 变量的值即为用户搜索的关键词, highlight用来对结果进行高亮
    {% highlight result.object.title with query %}
{% endfor%}

```
```html
参考代码如下
templates/search/search.html

{% extends 'base.html' %}
{% load highlight %}

{% block main %}
    {% if query %}
        {% for result in page.object_list %}
            <article class="post post-{{ result.object.pk }}">
                <header class="entry-header">
                    <h1 class="entry-title">
                        <a href="{{ result.object.get_absolute_url }}">{% highlight result.object.title with query %}</a>
                    </h1>
                    <div class="entry-meta">
                    <span class="post-category">
                        <a href="{% url 'blog:category' result.object.category.pk %}">
                            {{ result.object.category.name }}</a></span>
                        <span class="post-date"><a href="#">
                            <time class="entry-date" datetime="{{ result.object.created_time }}">
                                {{ result.object.created_time }}</time></a></span>
                        <span class="post-author"><a href="#">{{ result.object.author }}</a></span>
                        <span class="comments-link">
                        <a href="{{ result.object.get_absolute_url }}#comment-area">
                            {{ result.object.comment_set.count }} 评论</a></span>
                        <span class="views-count"><a
                                href="{{ result.object.get_absolute_url }}">{{ result.object.views }} 阅读</a></span>
                    </div>
                </header>
                <div class="entry-content clearfix">
                    <p>{% highlight result.object.body with query %}</p>
                    <div class="read-more cl-effect-14">
                        <a href="{{ result.object.get_absolute_url }}" class="more-link">继续阅读 <span
                                class="meta-nav">→</span></a>
                    </div>
                </div>
            </article>
        {% empty %}
            <div class="no-post">没有搜索到你想要的结果！</div>
        {% endfor %}
        {% if page.has_previous or page.has_next %}
            <div>
                {% if page.has_previous %}
                    <a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">{% endif %}&laquo; Previous
                {% if page.has_previous %}</a>{% endif %}
                |
                {% if page.has_next %}<a href="?q={{ query }}&amp;page={{ page.next_page_number }}">{% endif %}Next
                &raquo;{% if page.has_next %}</a>{% endif %}
            </div>
        {% endif %}
    {% else %}
        请输入搜索关键词，例如 django
    {% endif %}
{% endblock main %}
```
9. 在base.html中添加高亮的样式
```html
<head>
    <title>Black &amp; White</title>
    ...
    <style>
        span.highlighted {
            color: red;
        }
    </style>
    ...
</head>
```

10. 修改分词引擎
```python
#你安装的 haystack 中把 haystack/backends/whoosh_backends.py 文件拷贝到 blog/ 下，重命名为 whoosh_cn_backend.py，然后里面导入
from jieba.analyse import ChineseAnalyzer
#再将下面的代码
analyzer=StemmingAnalyzer()
#替换为
analyzer=ChineseAnalyzer()
```

11. 建立索引 python manage.py rebuild_index

