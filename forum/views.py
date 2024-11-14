from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Post, Comment, Like
from .forms import PostForm, CommentForm, RegistrationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404


def home(request):
    return render(request,  'forum/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'forum/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(
                request, 'Registration successful! You can now log in.'
                )
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'forum/register.html', {'form': form})


@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum/feed.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            messages.success(
                request, "Votre publication a été créée avec succès."
                )
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form})

# Vue pour commenter un post


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.profile
            comment.save()
            messages.success(request, "Commentaire ajouté.")
            return redirect('feed')
    else:
        form = CommentForm()
    return render(
        request, 'forum/add_comment.html', {'form': form, 'post': post}
        )

# Vue pour ajouter un "J'aime" à un post


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_profile = request.user.profile
    like, created = Like.objects.get_or_create(user=user_profile, post=post)
    if not created:
        like.delete()  # Si l'utilisateur a déjà aimé, on supprime le "J'aime"
    return redirect('feed')


def search_view(request):
    query = request.GET.get('q', '')
    if query:
        post_results = Post.objects.filter(Q(content__icontains=query))
        user_results = UserProfile.objects.filter(
            Q(user__username__icontains=query)
            )
        # Combinaison manuelle
        results = list(post_results) + list(user_results)
    else:
        results = []

    return render(
        request, 'forum/search_results.html',
        {'results': results, 'query': query}
        )


def user_profile(request, username):
    # Récupère l'utilisateur et le profil associé
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        raise Http404("Aucun profil utilisateur trouvé pour cet utilisateur.")
    posts = Post.objects.filter(author=user)
    followers_count = profile.followers.count() if hasattr(profile,
                                                           'followers') else 0
    following_count = profile.following.count() if hasattr(profile,
                                                           'following') else 0
    context = {
        'profile': profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'user_profile.html', context)


@login_required
def follow_user(request, user_id):
    profile_to_follow = get_object_or_404(UserProfile, user_id=user_id)
    user_profile = request.user.profile

    if user_profile != profile_to_follow:
        if user_profile.following.filter(id=profile_to_follow.id).exists():
            user_profile.following.remove(profile_to_follow)  # Se désabonner
        else:
            user_profile.following.add(profile_to_follow)  # S'abonner

    return redirect('user_profile', user_id=user_id)


def logout_view(request):
    logout(request)
    return redirect('home')
