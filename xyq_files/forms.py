from django import forms

from .models import Entry,Reply

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'receiver']
        labels = {
            'text': ' ',
            'receiver': ' '  # 设置为空格，因为我们会在模板中自定义显示
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80}),
            'receiver': forms.HiddenInput()  # 隐藏原始字段，使用自定义搜索框
        }
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text', 'receiver']
        widgets = {
            'receiver': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 80})
        }
        labels = {
            'text': ' ',
            'receiver': ' '
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80}),
            'receiver': forms.HiddenInput()  # 隐藏原始字段，使用自定义搜索框
        }