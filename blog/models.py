# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import django.utils.timezone as timezone
from mdeditor.fields import MDTextField
# 创建博文分类的表
class Category(models.Model):
	# 无需创建ID字段，django会自动创建
	# name是分类名的字段 charField是字段的数据类型，由于分类名字比较小所以用char，大小100就够用了
	name = models.CharField(max_length=100,verbose_name='分类名称')

	def __str__(self):
		return self.name
	class Meta:
		verbose_name="分类目录"
		verbose_name_plural = verbose_name



# 创建文章标签的表
class Tag(models.Model):
	# name是标签名的字段
	name = models.CharField(max_length=100,verbose_name='标签名称')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name="标签列表"
		verbose_name_plural = verbose_name

	def get_absolute_url(self):
		return reverse('blog:tag_list', kwargs={'pk': self.pk})


# 创建文章的类
class Post(models.Model):

	title = models.CharField(max_length=1000,verbose_name='标题')
	body = MDTextField(verbose_name='正文')
	# body = UEditorField(verbose_name="正文",width=600, height=300, toolbars="full", imagePath="post/ueditor", filePath="post/ueditor",default="")
	# 文章创建时间和修改时间
	created_time = models.DateTimeField(null=True,verbose_name='创建时间',default = timezone.now)
	modified_time = models.DateTimeField(verbose_name='修改时间',auto_now = True)
	# 文章摘要 blank参数是允许空值
	excerpt = models.CharField(max_length=300,blank=True,verbose_name='摘要')
	# 阅读量,类型只允许为整数或0，不得为负
	views = models.PositiveIntegerField(default=0)
	words = models.PositiveIntegerField(default=0)

	'''
        关联分类和标签的表
        一个分类可以有多篇文章，暂定一个文章智能有一个分类，所以用一对多的ForeignKey来关联
        一篇文章可以有多个标签，一个标签也可以有多篇文章，所以用多对多的ManyToManyField来关联
        定文章可以没有标签，因此为标签 tags 指定了 blank=True
	'''
	category = models.ForeignKey(Category,verbose_name='文章分类',on_delete=models.CASCADE)
	# tags = models.ManyToManyField(Tag,verbose_name='标签类型')
	tag = models.ManyToManyField(Tag,verbose_name='标签类型')

	'''
        文章作者
        这里 User 是从 django.contrib.auth.models 导入的。
        django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
        这里我们通过 ForeignKey 把文章和 User 关联了起来。
        因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
	'''
	author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE,default="reborn")

	def get_absolute_url(self):
		return reverse('blog:article', kwargs={'pk': self.pk})

	def __str__(self):
		return self.title

	# 阅读量增加1
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	def save(self, *args, **kwargs):
		if not self.excerpt:
			self.excerpt = strip_tags(self.body).replace("&nbsp;","")[:150] #strip_tags是去除html标签
		self.words = len(strip_tags(self.body).replace(" ","").replace('\n',""))	# 统计文章字数
		super(Post, self).save(*args, **kwargs) # 调用父类的 save 方法将数据保存到数据库中

	class Meta:
		verbose_name="文章列表"
		verbose_name_plural = verbose_name
