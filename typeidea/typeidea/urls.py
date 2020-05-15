"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, sitemaps
from django.contrib.sitemaps import views
from django.urls import path, re_path

from comment.views import CommentView
from .custom_site import custom_site

from blog.views import (IndexView, PostDetailView, CategoryView, TagView, SearchView, AuthorView,)
from config.views import LinkListView

from blog.rss import LatestPostFeed

from blog.sitemap import PostSitemap

"""
urlpatterns = [
    re_path(r'^$', post_list, name='index'),
    re_path(r'^category/(?P<category_id>\d+)/$', post_list, name='category-list'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'),
    re_path(r'^link/$', links, name='links'),
    re_path(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),
    path('admin/', custom_site.urls, name='admin'),
    path('super_admin/', admin.site.urls, name='super-admin')
]
"""
urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    re_path(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    re_path(r'^links/$', LinkListView.as_view(), name='links'),
    re_path(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    re_path(r'^search/$', SearchView.as_view(), name='search'),
    re_path(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name='author'),
    re_path(r'^comment/$', CommentView.as_view(), name='comment'),
    path('sitemap.xml', views.sitemap, {'sitemaps': {'posts': PostSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', custom_site.urls, name='admin'),
    path('super_admin/', admin.site.urls, name='super-admin'),
    path('rss/', LatestPostFeed(), name='rss'),

]
# re_path(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),