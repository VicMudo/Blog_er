from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post, SearchQuery
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:blog_home")

    def test_func(self):
        post = self.get_object()

        if post.author == self.request.user:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    new_comment = None
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.save()
    form = CommentForm()

    comments = post.comments.all()
    context = {'form': form, 'post': post, 'comments': comments}
    return render(request, 'blog/post_detail.html', context)

def search(request):
    query = request.GET.get('query', None)
    user = None

    if request.user.is_authenticated:
        user = request.user
    SearchQuery.objects.create(user=user, query=query)
    return render(request, 'blog/search.html', {'query': query})
