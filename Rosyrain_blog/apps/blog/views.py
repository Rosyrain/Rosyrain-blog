from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Blog, Tag, Category,Comment
from markdown import *
from pure_pagination import PageNotAnInteger, Paginator
from  apps.blog.forms import CommentForm

# Create your views here.

class IndexView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        all_category = Category.objects.all()
        all_tag = Tag.objects.all()
        for blog in all_blog:
            blog.content = markdown(blog.content, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blog, 5, request=request)  # 每页展示5篇
        all_blog = p.page(page)

        context = {
            'all_blog': all_blog,
        }
        print('all_bolg:', all_blog)
        return render(request, 'index.html', context)


class ArchiveView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        all_category = Category.objects.all()
        all_tag = Tag.objects.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blog, 5, request=request)  # 每页展示5篇
        all_blog = p.page(page)

        context = {
            'all_blog': all_blog,
            'all_category': all_category,
            'all_tag': all_tag,
        }
        return render(request, 'archive.html', context)


class TagView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        all_category = Category.objects.all()
        all_tag = Tag.objects.all()
        context = {
            'all_blog': all_blog,
            'all_category': all_category,
            'all_tag': all_tag,
        }

        return render(request, 'tags.html', context)


class TagDetailView(View):
    def get(self, request, tag_name):
        all_blog = Blog.objects.all().order_by('-id')
        all_category = Category.objects.all()
        all_tag = Tag.objects.all()

        tag = Tag.objects.filter(name=tag_name).first()
        tag_blogs = tag.blog_set.all()

        for blog in all_blog:
            blog.content = markdown(blog.content, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blog, 5, request=request)  # 每页展示5篇
        all_blog = p.page(page)

        context = {
            'all_blog': all_blog,
            'all_category': all_category,
            'all_tag': all_tag,
            'tag_name': tag_name,
            'tag_blogs': tag_blogs,
        }

        return render(request, 'tag_detail.html', context)


class BlogDetailView(View):
    def get(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        all_comment = Comment.objects.all()
        blog.content = markdown(blog.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True

        # 将状态码与上下博客传递给前端页面
        context = {
            'blog': blog,
            'blog_prev': blog_prev,
            'blog_next': blog_next,
            'has_prev': has_prev,
            'has_next': has_next,
            'all_comment':all_comment,

        }
        return render(request, 'blog_detail.html', context)


class AddCommentView(View):
    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class CategoryDetaiView(View):
    def get(self, request, category_name):
        category = Category.objects.filter(name=category_name).first()
        cate_blogs = category.blog_set.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(cate_blogs, 5, request=request)
        cate_blogs = p.page(page)

        context = {
            'cate_blogs': cate_blogs,
            'category_name': category_name,
        }

        return render(request, 'category_detail.html',context )