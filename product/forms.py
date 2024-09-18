from django import forms
from .models import Comment,Product,Catigory
from users.models import User

class CommentForm(forms.ModelForm):
    start_give=forms.IntegerField(max_value=5,min_value=1)
    comment_text=forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    class Meta:
        model=Comment
        fields=('comment_text','start_give')

class AddKitob(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            self.fields['user'].initial = request.user
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # catigory = forms.ModelChoiceField(queryset=Catigory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}))
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Product
        fields = '__all__'

    

class AddTilForm(forms.ModelForm):

    class Meta:
        model=Catigory
        fields='__all__'