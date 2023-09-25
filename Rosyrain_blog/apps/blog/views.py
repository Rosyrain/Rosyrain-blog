from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Blog, Tag, Category,Comment,Counts
from markdown import *
from pure_pagination import PageNotAnInteger, Paginator
from  apps.blog.forms import CommentForm
from Rosyrain_blog.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
from haystack.views import SearchView
# Create your views here.

class IndexView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
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
            'blog_nums':blog_nums,
            'cate_nums':cate_nums,
            'tag_nums':tag_nums,
        }
        print('all_bolg:', all_blog)
        return render(request, 'index.html', context)


class ArchiveView(View):
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blog, 5, request=request)  # 每页展示5篇
        all_blog = p.page(page)

        context = {
            'all_blog': all_blog,
            'blog_nums':blog_nums,
            'cate_nums':cate_nums,
            'tag_nums':tag_nums,
        }
        return render(request, 'archive.html', context)


class TagView(View):
    def get(self, request):
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        all_tag = Tag.objects.all()


        context = {
            'blog_nums':blog_nums,
            'cate_nums':cate_nums,
            'tag_nums':tag_nums,
            'all_tag': all_tag,
        }

        return render(request, 'tags.html', context)


class CategoryView(View):
    def get(self, request):
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        all_cate = Category.objects.all()
        context = {
            'blog_nums':blog_nums,
            'cate_nums':cate_nums,
            'tag_nums':tag_nums,
            'all_cate': all_cate,
        }

        return render(request, 'category.html', context)


class TagDetailView(View):
    def get(self, request, tag_name):
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        tag = Tag.objects.filter(name=tag_name).first()
        tag_blogs = tag.blog_set.all()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(tag_blogs, 5, request=request)
        tag_blogs = p.page(page)

        #print(tag_blogs)

        context = {
            'blog_nums':blog_nums,
            'cate_nums':cate_nums,
            'tag_nums':tag_nums,
            'tag_name': tag_name,
            'tag_blogs': tag_blogs,
        }

        return render(request, 'tag_detail.html', context)


class BlogDetailView(View):
    def get(self, request, blog_id):
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums


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
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

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


class CategoryDetailView(View):
    def get(self, request, category_name):
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

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
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

        }

        return render(request, 'category_detail.html',context )

class MySearchView(SearchView):

    def build_page(self):
        #分页重写
        super(MySearchView, self).extra_context()

        try:
            page_no = int(self.request.GET.get('page', 1))
        except PageNotAnInteger:
            raise HttpResponse("Not a valid number for page.")

        if page_no < 1:
            raise HttpResponse("Pages should be 1 or greater.")


        paginator = Paginator(self.results, HAYSTACK_SEARCH_RESULTS_PER_PAGE, request=self.request)
        page = paginator.page(page_no)

        return (paginator, page)