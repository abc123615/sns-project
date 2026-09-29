from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm


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

    return render(
        request,
        'posts/post_detail.html',
        {'post': post}
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