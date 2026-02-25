from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post, User


POSTS_PER_PAGE = 10


def add_comment_count_annotation(queryset):
    return queryset.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def filter_published_posts(posts=None):
    if posts is None:
        posts = Post.objects.all()
    return posts.select_related('author', 'category', 'location').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def paginate_posts(posts, request):
    return Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get('page'))


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = add_comment_count_annotation(filter_published_posts())
    paginate_by = POSTS_PER_PAGE


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user.username])


class PostDetailView(PostMixin, DetailView):

    def get_object(self):
        object = super().get_object()
        if not (
            filter_published_posts(Post.objects.filter(pk=object.pk)).exists()
        ) and object.author != self.request.user:
            raise Http404("Пост не найден")
        return object

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            form=CommentForm(),
            comments=self.object.comments.select_related('author')
        )


class PostUpdateView(OnlyAuthorMixin, PostMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(OnlyAuthorMixin, PostMixin, DeleteView):
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.author])


class CategoryPostsListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_PER_PAGE

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return add_comment_count_annotation(
            filter_published_posts(self.get_category().posts)
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, category=self.get_category())


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


class CommentMixin:
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['comment_id']])


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
        return super().get_context_data(
            **kwargs,
            page_obj=paginate_posts(
                add_comment_count_annotation(self.object.posts.all()),
                self.request
            )
        )


class UserUpdateView(UserPassesTestMixin, UserMixin, UpdateView):
    form_class = UserForm
    template_name = 'blog/user_form.html'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.kwargs['username']])
