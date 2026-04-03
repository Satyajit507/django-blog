from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Blog, Category

# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belongs to the category with the id category_id
    posts = Blog.objects.filter(status='published',category=category_id)
    try:
       category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    context ={
        'posts': posts,
        'category':category,
    }
    return render(request,'posts_by_category.html', context)
