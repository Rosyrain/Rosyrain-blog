from django.contrib import admin
from django.urls import path, re_path, include
from .views import IndexView, ArchiveView, TagView, TagDetailView, BlogDetailView, AddCommentView, CategoryDetaiView
from apps.blog.feeds import BlogRssFeed

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),  # 首页
    re_path(r'^archive/$', ArchiveView.as_view(), name='archive'),  # 归档，按日期分类
    re_path(r'^tags/$', TagView.as_view(), name='tags'),  # 标签云界面
    re_path(r'^tags/(?P<tag_name>\w+)$', TagDetailView.as_view(), name='tag_name'),  # 具体标签页，包含该标签下的博客
    re_path(r'^blog/(?P<blog_id>\d+)$', BlogDetailView.as_view(), name='blog_id'),  # 具体博客页，展示博客内容
    re_path(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),  # 评论添加
    re_path(r'^rss/$', BlogRssFeed(), name='rss'),  # rss订阅
    re_path(r'^category/(?P<category_name>\w+)/$', CategoryDetaiView.as_view(), name='category_name'),  # 具体分类页，包含该分类的博客

]
