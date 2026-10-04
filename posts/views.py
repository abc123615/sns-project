from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import PostForm, ProfileForm, CommentForm
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(
        request,
        'posts/post_list.html',
        {'posts': posts}
    )


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    return render(
        request,
        'posts/post_detail.html',
        {'post': post, 'form': form}
    )

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'posts/post_edit.html',
        {'form': form, 'post': post}
    )

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(
        request,
        'posts/post_confirm_delete.html',
        {'post': post}
    )

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=profile.user).order_by('-created_at')

    return render(
        request,
        'posts/profile.html',
        {
            'profile': profile,
            'posts': posts
        }
    )

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'posts/profile_edit.html',
        {'form': form}
    )

@login_required
@require_POST
def follow_toggle(request, username):
    target_profile = get_object_or_404(
        Profile,
        user__username=username
    )

    my_profile = get_object_or_404(
        Profile,
        user=request.user
    )
    if target_profile == my_profile:
        return redirect('profile', username=username)

    if target_profile in my_profile.following.all():
            my_profile.following.remove(target_profile)
    else:
            my_profile.following.add(target_profile)

    return redirect('profile', username=username)

@login_required
def following_list(request, username):
    profile = get_object_or_404(
        Profile,
        user__username=username
    )

    following = profile.following.all()

    return render(
        request,
        'posts/following_list.html',
        {
            'profile': profile,
            'following': following
        }
    )

@login_required
def followers_list(request, username):
    profile = get_object_or_404(
        Profile,
        user__username=username
    )

    followers = profile.followers.all()

    return render(
        request,
        'posts/followers_list.html',
        {
            'profile': profile,
            'followers': followers
        }
    )

@login_required
def following_posts(request):
    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    following_users = profile.following.values_list(
        'user',
        flat=True
    )

    posts = Post.objects.filter(
        author__in=list(following_users) + [request.user.id]
    ).order_by('-created_at')

    return render(
        request,
        'posts/post_list.html',
        {
            'posts': posts,
            'following_only': True
        }
    )

@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(
        Comment, pk=pk, author=request.user
    )
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'posts/comment_edit.html',
        {'form': form, 'comment': comment}
    )

@login_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(
        Comment,
        pk=pk,
        author=request.user
    )
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk=post_pk)