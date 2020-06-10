import mistune
from django import forms

from comment.models import Comment

class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            # attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            # attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=50,
        widget=forms.widgets.URLInput(
            # attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            # attrs={'rows': 6, 'cols': 80, }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # name不能省掉，否则会报错：'tuple' object has no attribute 'widget'
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "width: 60%;"
            if field.label == '内容':
                field.widget.attrs['placeholder'] = "支持MarkDown格式"
            else:
                field.widget.attrs['placeholder'] = "请输入%s" % (field.label)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('内容长度不少于5个字!')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']



