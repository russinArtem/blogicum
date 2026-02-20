from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post, User


def filter_published_posts(posts):
    return posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = filter_published_posts(Post.objects.all())
    paginate_by = 10


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        post_id = self.kwargs.get('post_id')
        return redirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': post_id}
        ))


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'
    slug_field = 'id'


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(PostMixin, DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_published and self.object.author != request.user:
            raise Http404("Пост не найден")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(OnlyAuthorMixin, PostMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(OnlyAuthorMixin, PostMixin, DeleteView):
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.author}
        )


class CategoryPostsListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10
    slug_url_kwarg = 'category_slug'
    slug_field = 'category'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return filter_published_posts(self.category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentMixin:
    model = Comment
    slug_url_kwarg = 'comment_id'
    slug_field = 'id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class CommentUpdateView(OnlyAuthorMixin, CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(OnlyAuthorMixin, CommentMixin, DeleteView):
    template_name = 'blog/comment_form.html'


class UserMixin:
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'


class UserDetailView(UserMixin, DetailView):
    template_name = 'blog/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class UserUpdateView(UserPassesTestMixin, UserMixin, UpdateView):
    form_class = UserForm
    template_name = 'blog/user_form.html'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )
