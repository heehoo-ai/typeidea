from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Tag, Post


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', )
    fields = ('name', 'status', 'is_nav')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 展示页面
    list_display = [
        'title',  'category',  'status', 'created_time', 'operator'
    ]
    list_display_links = ['title']
    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    fields = (
        'category', 'title',
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))

        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
