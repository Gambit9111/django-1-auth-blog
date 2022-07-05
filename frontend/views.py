from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from frontend.models import Post
from frontend.forms import PostForm
from django.contrib.auth.models import User, Group

# Create your views here.

def index(request):
    return render(request, 'frontend/index.html')

@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("auth.add_user")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.has_perm("auth.add_user"):
                try:
                    group = Group.objects.get(name='user')
                    group.user_set.remove(user)
                except:
                    pass
    return render(request, 'frontend/home.html', {'posts': posts})


@login_required(login_url='login')
@permission_required("frontend.add_post", login_url='login', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'frontend/create_post.html', {'form': form})