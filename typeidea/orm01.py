
import os
import sys



import typeidea

if __name__ == '__main__':
    from typeidea import wsgi

    import django
    django.setup()

    from blog import models
    # 查询所有文章的id和title
    # ret = models.Post.objects.all().values('id', 'title')
    # print(ret)

    # 查询所属“Django”分类中有多少篇文章
    # ret = models.Category.objects.get(name='Django').post_set.count()
    # print(ret)
    # 查询所属“Django”分类中有多少篇文章 聚合查询方法
    # 只要是两个model类通过 ForeignKey或者ManyToMany关联起来，就使用 annotate方法来统计数量
    # from django.db.models import Count
    # categories = models.Category.objects.annotate(posts_count=Count('post'))
    # tags = models.Tag.objects.annotate(posts_count=Count('post'))
    # print(categories[0].posts_count, tags[8].posts_count)

    # 查询分类为“Django”的文章
    # post_list = models.Category.objects.get(name="Django").post_set.filter(status=models.Post.STATUS_NORMAL)
    # print(post_list)

    # 查询所有文章的题目、作者及分类，使用select_related优化查询, 解决N+1问题
    # post_list = models.Post.objects.filter(status=models.Post.STATUS_NORMAL) # 执行了4次查询
    # post_list = models.Post.objects.filter(status=models.Post.STATUS_NORMAL).select_related('category', 'owner') # 执行了2次查询
    # print(post_list[0].category, post_list[0].owner)

    import json
    s = '{"name":"hehu", "age":38}'
    # 把字符串反序列化成Python的数据类型
    ret = json.loads(s)
    print(ret, type(ret))
    # 把字典序列化成python字符串
    ret_str = json.dumps(ret)
    print(ret_str, type(ret_str))