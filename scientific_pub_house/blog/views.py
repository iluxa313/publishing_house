from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from blog.models import Post, Magazine, User, Comment
from .forms import PostForm, CommentForm, UserForm


class PostListView(ListView):
    model = Post
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.select_related('magazine', 'author').filter(
            is_published=True,
            magazine__is_published=True,
            pub_date__lte=now(),
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return queryset


class MagazineListView(ListView):
    paginate_by = 6
    model = Magazine

    def get_queryset(self):
        magazine = get_object_or_404(
            Magazine,
            slug=self.kwargs['magazine'],
            is_published=True
        )

        queryset = Post.objects.select_related('author', 'magazine').order_by('-pub_date').filter(
            magazine=magazine,
            is_published=True,
            pub_date__lte=now()
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['magazine'] = get_object_or_404(
            Magazine,
            slug=kwargs['magazine'],
            is_published=True
        )
        return context


class UserPostListView(ListView):
    template_name = 'users/customuser_list.html'
    paginate_by = 6
    model = User
    user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(
            User, username=kwargs['username']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.select_related('magazine', 'author').order_by('-pub_date').filter(
            author=self.user,
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.user
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    current_user = None

    def dispatch(self, request, *args, **kwargs):
        self.current_user = get_object_or_404(
            User,
            pk=kwargs['pk'],
            username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile_detail', kwargs={'username': self.current_user.username})


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        return Post.objects.select_related('magazine', 'author').get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        context['form'] = CommentForm()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if request.user != post.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'blog/post_form.html'
    model = Post

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile_detail', kwargs={'username': self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    current_post = None

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.current_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.current_post.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/comment_form.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs['id'],
            post__pk=self.kwargs['pk']
        )
        if request.user != comment.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_form.html'
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comment, pk=kwargs['id'], post__pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})
