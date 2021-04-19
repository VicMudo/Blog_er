from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView,
    UpdateView, DeleteView, FormView
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Comment, Post
from .forms import CommentForm, EmailFeedbackForm


def welcome(request):
    return render(request, 'blog/welcome.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4
    

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


class PostDisplayView(DetailView):
    model = Post
    
    def get_object(self):
        object = super(PostDisplayView, self).get_object()
        object.view_count += 1
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(PostDisplayView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object())
        context['form'] = CommentForm()
        return context


class CommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        if self.request.is_ajax:    
            post = Post.objects.get(pk=self.kwargs['pk'])
            form.instance.post = post
            obj = form.save()
            res = [{"name": obj.name, "created": obj.created, "body": obj.body}]
            return JsonResponse(res, safe=False)
        return super(CommentView, self).form_valid(form)
        
    def get_success_url(self):
       return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)

def handle_feedback_email(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sender_email = request.user.email
            message = request.POST['message']
            send_mail("Viewer Feedback",
                    message,
                    sender_email,
                    ['victory@hotmail.io'],
                    fail_silently=False
            )
            return redirect('blog:blog_home')
    else:
        if request.method == 'POST':
            sender_email = request.POST['email']
            message = request.POST['message']
            send_mail("Viewer Feedback",
                        message,
                        sender_email,
                        ['victory@hotmail.io'],
                        fail_silently=False
                    )
            return redirect('blog:blog_home')
            