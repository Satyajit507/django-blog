
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


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