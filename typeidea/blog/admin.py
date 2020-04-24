from typeidea.custom_site import custom_site
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Tag, Post
from django.contrib.auth.models import User
from .adminforms import PostAdminForm


# Register your models here.


# class PostInline(admin.StackedInline):  # admin.TabularInline是横向排列的样式
#     fields = ('title', 'desc', 'owner')
#     extra = 1
#     model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', )
    fields = ('name', 'status', 'is_nav')
    # inlines = [PostInline, ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', )


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类"""
    title = "分类"
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        return Category.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            # return queryset.filter(category_id=self.value(), owner=request.user)
            return queryset.filter(category_id=self.value())
        return queryset


class OwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户"""
    title = "作者"
    parameter_name = 'owner_id'

    def lookups(self, request, model_admin):
        return User.objects.values_list('id', 'username')

    def queryset(self, request, queryset):
        owner_id = self.value()
        if owner_id:
            return queryset.filter(owner_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    # 展示页面
    form = PostAdminForm
    list_display = [
        'title',  'category',  'status', 'owner', 'created_time', 'operator'
    ]
    list_display_links = ['title']
    # list_filter = [CategoryOwnerFilter, OwnerFilter]
    list_filter = ['owner', 'category']
    search_fields = ['title', 'category__name']
    filter_horizontal = ('tag',)
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    exclude = ('owner',)
    # fields = ('category', 'title',  'desc',  'status',  'content', 'tag', )
    fieldsets = (
        (
            "基础配置", {
                'description': '*',
                'fields': (
                    ('title', 'category'),
                    'status',
                ),
            }
        ),
        (
            '内容', {
                'fields': (
                    'desc',
                    'content',
                )
            }
        ),
        (
            '额外信息', {
                'classes': ('collapse',),
                'fields': ('tag',),
            }
        )

    )


    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))

        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    class Media:
        css = {
            "all": ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)