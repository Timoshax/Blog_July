from django.shortcuts import render, redirect
from .models import Post, PostAttachment, Comment
from .form import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.
def post_list(request):
    posts = Post.objects.order_by('-time_stamp')
    for post in posts:
        images = PostAttachment.objects.filter(post_id = post.pk)
        post.att = images
        comments = Comment.objects.filter(post_id = post.pk)
        post.comments = comments
    return render(request, 'post/post_list.html', {'posts' : posts})
def post_details(request, pid):
    post = Post.objects.get(pk = pid)
    images = PostAttachment.objects.filter(post_id = pid)
    return render(request, 'post/post_details.html', {'post':post , 'images':images})

@login_required
def add_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        att = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            for img in att:
                PostAttachment.objects.create(post_id = post.pk, file=img)
            return redirect(to= 'post_details', pid = post.pk)
    return render(request, 'post/new_post.html', {'form': form})
@login_required
def edit_post(request, pid):
    post = Post.objects.get(pk = pid)

    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden('У вас нет прав на редактирования этого поста')

    post_att = PostAttachment.objects.filter(post_id = pid)
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(request.POST, instance= post)
        if form.is_valid():
            post = form.save(commit = False)
            att = request.FILES.getlist('images')
            for img in att:
                PostAttachment.objects.create(post_id = pid, file = img)
            chosen = request.POST.getlist('attachments')
            for img_id in chosen:
                PostAttachment.objects.get(pk = img_id).delete()
            post.edited = True
            post.save()

        return redirect(to='post_details', pid = post.pk)
    return render(request, 'post/edit_post.html', {'form':form, 'post_att': post_att})
@login_required
def delete_post(request, pid):
    post = Post.objects.get(pk = pid)
    post.delete()
    return redirect(to = 'post_list')