from .models import Post, User, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
