from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body',)

class EmailFeedbackForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())