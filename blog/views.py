from django.shortcuts import render,redirect
from .models import Post,User,PostUpdateForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import CreateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


# Authenticating user if he is logged in
@login_required(login_url='/')

# Loading home view
def home(request):

    # User clicked on search button
    if request.method == 'POST':

        sub_name = request.POST['SearchBar']
        posts = Post.objects.all().order_by('-date_posted')
        post_list = []
        
        #Creating a list of subject user searched for
        for post in posts:
            if post.title == sub_name:
                post_list.append(post)
        context = {'posts' : post_list}

        # List is not empty
        if len(post_list) != 0:
            return render(request,'blog_temp/home.html', context)
        # List is empty
        else:
            messages.warning(request, f'No posts found named {sub_name}')
            return render(request,'blog_temp/home.html')

    # Loading all the posts
    posts = Post.objects.all().order_by('-date_posted')
    context = {'posts' : posts}
    return render(request, 'blog_temp/home.html', context)


# Authenticating user if he is logged in
@login_required(login_url='/')

# Display the list of posts whose author is logged in user.
def myPost(request):
    user = User.objects.get(username=request.user.username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {'posts' : posts}
    return render(request, 'blog_temp/myPost.html', context)


# Authenticating user if he is logged in
@login_required(login_url='/')

# User clicked on delete post button
def post_delete(request, pk):

    # Getting the right post by primary key
    user = User.objects.get(username=request.user.username)
    post = get_object_or_404(Post, pk=pk)

    # Checking if the user is author of the post
    if user == post.author:
        messages.success(request, f'{post.title} post has been deleted.')
        post.delete()

    # User is not the author of the post
    else:
        messages.warning(request, 'You are not authorized to update this post.')

    return redirect('blog-myPost')


# Authenticating user if he is logged in
@login_required(login_url='/')

# User clicked on update post button
def post_update(request, pk):

    # User clicked on update button on update post page
    if request.method == 'POST':

        post = get_object_or_404(Post, pk=pk)
        form = PostUpdateForm(request.POST,instance=post)

        # If post's form is valid save the update
        if form.is_valid():
            form.save()
            messages.success(request,f'{post.title} post has been updated.')
            return redirect('blog-myPost')

    else:
        post = get_object_or_404(Post, pk=pk)
        form = PostUpdateForm(instance=post)

    # Getting the logged in username
    user = User.objects.get(username=request.user.username)
    post = get_object_or_404(Post, pk=pk)

    # Logged in user is the author of post
    if user == post.author:
        context = {'form' : form}
        return render(request, 'blog_temp/update_post.html',context)
    
    # Logged in user is not the author of the post
    else:
        messages.warning(request,'You are not authorized to update this post.')
        return redirect('blog-myPost')


# Authenticating user if he is logged in
@login_required(login_url='/')

# User clicked on post's author profile
def authorProfile(request, author):

    user = User.objects.get(username=request.user.username)

    # User is the author of the post redirect to user-porfile page
    if str(user) == str(author):
        return redirect('user-profile')

    # Getting the author data to display
    authorData = User.objects.get(username=author)
    context = {'author' : authorData}
    return render(request, 'blog_temp/author_profile.html', context)


# Authenticating user if he is logged in
@method_decorator(login_required, name='dispatch')

# Creating a form view for user to add new post
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog_temp/add_post.html'

    # Setting the author of user logged in user
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Authenticating user if he is logged in
@login_required(login_url='/')

# Logging out the current user.
def logout_user(request):
    logout(request)
    messages.success(request,'You are Logged Out.')
    return redirect('user-login')