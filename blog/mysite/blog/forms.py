from django import forms
from .models import comment

class CommentForms(forms.ModelForm):
    class Meta:
        model =comment
        fields = ("name","body","email")


class SearchForm(forms.Form):
    query = forms.CharField()
    
class EmailPostForm(forms.Form):
    name =forms.CharField(max_length=50)
    Email = forms.EmailField()
    to =forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea , required=False)    