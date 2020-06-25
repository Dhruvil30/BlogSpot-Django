from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from .models import UserUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Method for loggind in user
def login_user (request):

    # User clicked on 'Sign in' button
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        # Authenticating user
        user = authenticate(request, username=username, password=password)

        # User is authenticated
        if user is not None:
            login(request, user)
            return redirect('blog-home')

        # User is not authenticated
        else:
            messages.warning(request,'Username or Password is wrong.')

    return render(request, 'user_temp/login_page.html')

# Method to register user
def register_user(request):

    # User click on 'Register' button
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Form is valid
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created For {username}.')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()

    return render(request, 'user_temp/register_page.html',{'form':form})


# Authenticating user if he is logged in
@login_required(login_url='/')

# Method to display and update user profile
def profile(request):

    # User clicked on 'Update' button
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        # From is valid
        if form.is_valid():
            form.save()
            messages.success(request,'Your account data has been updated.')
            return redirect('user-profile')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {'form' : form}
    return render(request, 'user_temp/profile.html',context)

# Authenticating user if he is logged in
@method_decorator(login_required, name='dispatch')

# Creating profile view
class ProfileView(CreateView):

    model = User
    fields = ['username', 'email']
    template_name = 'user_temp/profile.html'
    