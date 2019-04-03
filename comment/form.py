from django import forms

class CommentForm(forms.Form):
    content_type =forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)