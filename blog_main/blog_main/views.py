
from django.shortcuts import render, redirect
from blogs.models import Blog, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def home(request):

    featured_posts = Blog.objects.filter(is_featured=True, status='published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status ='published')
    
    context={
        
        'featured_posts': featured_posts,
        'posts':posts,
    }
    return render(request, 'home.html',context)


def search(request):
    keyword = request.GET.get('keyword')
    return render(request, 'home.html', {'keyword': keyword})


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')