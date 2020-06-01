from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from django.views.generic import TemplateView

from comment.forms import CommentForm
from .models import Comment


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request):
        # 接受form表单提交的数据
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')  # /post/23.html
        import re
        target_post_id = re.findall(r"\d+", target)

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.target_post_id = int(target_post_id[0])

            instance.save()
            succeed = True
            return redirect(target)  # ?
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }

        return render(request, self.template_name, context=context)
