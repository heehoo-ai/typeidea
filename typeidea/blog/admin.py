from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Tag, Post
from django.contrib.auth.models import User

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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 展示页面
    list_display = [
        'title',  'category',  'status', 'owner', 'created_time', 'operator'
    ]
    list_display_links = ['title']
    # list_filter = [CategoryOwnerFilter, OwnerFilter]
    list_filter = ['owner', 'category']
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

    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的服务器"""
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
