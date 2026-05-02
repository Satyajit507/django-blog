from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import Blog, Category, Comment, Notification


# 📂 POSTS BY CATEGORY
def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status='published', category=category_id)
    category = get_object_or_404(Category, pk=category_id)

    return render(request, 'posts_by_category.html', {
        'posts': posts,
        'category': category
    })


# 📖 BLOG DETAIL + COMMENTS + REPLIES
def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='published')

    # 💬 ADD COMMENT / REPLY
    if request.method == 'POST':
        text = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')

        parent_obj = None
        if parent_id:
            parent_obj = Comment.objects.get(id=parent_id)

        comment = Comment.objects.create(
            user=request.user,
            blog=single_blog,
            comment=text,
            parent=parent_obj
        )

        # 🔔 NOTIFICATIONS
        if parent_obj:
            if parent_obj.user != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=parent_obj.user,
                    comment=parent_obj,
                    notif_type='reply'
                )
        else:
            if single_blog.author != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=single_blog.author,
                    blog=single_blog,
                    notif_type='comment'
                )

        return HttpResponseRedirect(request.path_info)

    # 💬 ONLY MAIN COMMENTS (NO REPLIES HERE)
    comments = Comment.objects.filter(
    blog=single_blog,
    parent=None
).prefetch_related('replies', 'user')

    comment_count = Comment.objects.filter(blog=single_blog).count()

    return render(request, 'blogs.html', {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count
    })


# ❤️ LIKE COMMENT (AJAX + NOTIFICATION)
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

        # 🔔 notification
        if comment.user != request.user:
            Notification.objects.create(
                sender=request.user,
                receiver=comment.user,
                comment=comment,
                notif_type='like'
            )

    return JsonResponse({
        'liked': liked,
        'total_likes': comment.likes.count()
    })


# 🔍 SEARCH
def search(request):
    keyword = request.GET.get('keyword')

    blogs = Blog.objects.filter(
        Q(title__icontains=keyword) |
        Q(short_description__icontains=keyword) |
        Q(blog_body__icontains=keyword),
        status='published'
    )

    return render(request, 'search.html', {
        'blogs': blogs,
        'keyword': keyword
    })