from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # after signup → login page
    else:
        form = UserCreationForm()
    return render(request, "blogapp/registration/signup.html", {"form": form})

# ✅ FBV for homepage
def home(request):
    return render(request, 'blogapp/home.html')

# ✅ ListView
class PostListView(ListView):
    model = Post
    template_name = 'blogapp/post_list.html'  # default: <app>/<model>_list.html
    context_object_name = 'posts'
    ordering = ['-created_at']  # latest first

# ✅ DetailView
class PostDetailView(DetailView):
    model = Post
    template_name = 'blogapp/post_detail.html'

# ✅ CreateView
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blogapp/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "✅ Post created successfully!")
        return super().form_valid(form)

# ✅ UpdateView (only author can update)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blogapp/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "✏️ Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ✅ DeleteView (only author can delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogapp/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
