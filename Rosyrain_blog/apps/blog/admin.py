from django.contrib import admin
from apps.blog.models import Blog,Category,Tag,Comment
# Register your models here.

#admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'click_count', 'category', 'create_time', 'update_time']

    def save_model(self, request, obj, form, change):
        obj.save()
        #博客分类数目统计
        obj_category = obj.category
        category_count = obj_category.blog_set.count()
        obj_category.count = category_count
        obj_category.save()
        #博客标签数目统计
        obj_tag_list = obj.tag.all()
        for obj_tag in obj_tag_list:
            tag_count = obj_tag.blog_set.count()
            obj_tag.count = tag_count
            obj_tag.save()

    def delete_model(self, request, obj):
        obj.delete()
        #博客分类数目统计
        obj_category = obj.category
        category_count = obj_category.blog_set.count()
        obj_category.count = category_count
        obj_category.save()
        #博客标签数目统计
        obj_tag_list = obj.tag.all()
        for obj_tag in obj_tag_list:
            tag_count = obj_tag.blog_set.count()
            obj_tag.count = tag_count
            obj_tag.save()


admin.site.register(Blog,BlogAdmin)