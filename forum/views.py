from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Post, Like, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm

def home(request):
    return render(request, 'forum\home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('thread_list')  # Redirige vers la liste des threads
        else:
            # Gérer l'erreur de connexion
            return render(request, 'login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    return render(request, 'templates\forum\login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'templates\forum\register.html', {'form': form})
@login_required
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'thread_list.html', {'threads': threads})
@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()
    return render(request, 'thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Inclure FILES pour le téléchargement d'images
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('thread_detail', pk=post.thread.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        thread = Thread.objects.create(title=title, author=request.user)
        return redirect('thread_detail', thread_id=thread.id)
    return render(request, 'create_thread.html')

@login_required
def add_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(content=content, author=request.user, thread=thread)
        return redirect('thread_detail', thread_id=thread.id)
    return render(request, 'add_post.html', {'thread': thread})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        # Assuming you have a Comment model (not defined in previous context)
        Comment.objects.create(content=content, author=request.user, post=post)
        return redirect('thread_detail', thread_id=post.thread.id)
    return render(request, 'add_comment.html', {'post': post})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    threads = Thread.objects.filter(author=user)
    return render(request, 'user_profile.html', {'user': user, 'threads': threads})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    # Logic to follow the user (not defined in previous context)
    return redirect('user_profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    # Logic to unfollow the user (not defined in previous context)
    return redirect('user_profile', user_id=user_id)

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Remove like if it already exists
    return redirect('thread_detail', thread_id=post.thread.id)

def logout_view(request):
    logout(request)
    return redirect('home')