from dal import autocomplete
from django import forms

from blog.models import Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')

        widgets = {
            'category': autocomplete.ModelSelect2(url='category-autocomplete'),
            'tag': autocomplete.ModelSelect2Multiple(url='tag-autocomplete')
        }

