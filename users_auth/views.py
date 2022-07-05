from django.shortcuts import render, redirect
from frontend.models import Post
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='user')
            group.user_set.add(user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
@permission_required("auth.add_user", login_url='login', raise_exception=True)
def moderator(request):

    if request.user.has_perm("auth.can_add_administrator"):
        users = User.objects.exclude(groups__name='owner')

    elif request.user.has_perm("auth.can_add_moderator"):
        users = User.objects.exclude(groups__name='owner').exclude(groups__name='administrator')

    elif request.user.has_perm("auth.add_user"):
        users = User.objects.exclude(groups__name='owner').exclude(groups__name='administrator').exclude(groups__name='moderator')
        

    #get 'user.id'
    if request.method == "POST":
        user_id_delete_posts = request.POST.get('user-id-delete-posts')
        user_id_delete_user = request.POST.get('user-id-delete-user')

        if user_id_delete_posts:
            user = User.objects.filter(id=user_id_delete_posts).first()
            print(user)
            posts = Post.objects.filter(author=user)
            print(posts)
            posts.delete()

        elif user_id_delete_user:
            user = User.objects.filter(id=user_id_delete_user).first()
            print(user)
            user.delete()
            

    return render(request, 'users_auth/mod_panel.html', {'users': users})


@login_required(login_url='login')
def posts(request, user_id):
    user = User.objects.filter(id=user_id).first()
    posts = Post.objects.filter(author=user)
    print(posts)
    return render(request, 'users_auth/user_posts.html', {'posts': posts, 'user': user})



def create_admin(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            group = Group.objects.get(name='administrator')
            group.user_set.add(user)
            return redirect('moderator')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def create_mod(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='moderator')
            group.user_set.add(user)
            return redirect('moderator')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})