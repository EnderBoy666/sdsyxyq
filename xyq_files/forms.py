from django import forms

from .models import Entry,Reply

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':' '}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        labels = {'text':' '}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}