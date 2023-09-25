from django.db import models

# Create your models here.
class Category(models.Model):
    '''
    文章分类
    '''
    name = models.CharField(max_length=20,verbose_name='文章类别')
    count = models.IntegerField(default=0,verbose_name='分类数目')


    class Meta:
        verbose_name = '文章类别'

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    '''
    文章标签
    '''
    name = models.CharField(max_length=20,verbose_name='文章标签')
    count = models.IntegerField(default=0,verbose_name='标签数目')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    content = models.TextField(default=' ',verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    click_count = models.IntegerField(default=0 ,verbose_name='点击量')
    category = models.ForeignKey(Category,verbose_name='文章类别',on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,verbose_name='文章标签')


    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class Comment(models.Model):

    name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name='内容', max_length=300)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(Blog, verbose_name='博客',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]

class Counts(models.Model):
    """
    统计博客、分类和标签的数目
    """
    blog_nums = models.IntegerField(verbose_name='博客数目', default=0)
    category_nums = models.IntegerField(verbose_name='分类数目', default=0)
    tag_nums = models.IntegerField(verbose_name='标签数目', default=0)
    visit_nums = models.IntegerField(verbose_name='网站访问量', default=0)


    class Meta:
        verbose_name = '数目统计'
        verbose_name_plural = verbose_name