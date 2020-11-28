from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body',)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea())