from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from my_app.forms import LoginForm, SignupForm, UpdateUserForm, UserInfoForm, ChangePasswordForm, \
    InterpreterApplicationForm
from my_app.models import Profile


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about-us.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact-us.html')


def gallery(request):
    return render(request, 'gallery.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def interpreters(request):
    return render(request, 'interpreters.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # do some shopping cart retrieval
                # current_user = Profile.objects.get(user__id=user.id)
                # get saved cart from it
                # saved_cart = current_user.old_cart
                # convert db string to python dictionary
                # if saved_cart:
                #     # convert using json
                #     converted_cart =  json.loads(saved_cart)
                #     # add loaded dictionary to cart
                #     # cart = Cart(request)
                #     # loop through the cart and add items from db
                #     for key, value in converted_cart.items():
                #         cart.db_add(product=key, quantity=value)
                # messages.success(request, "You are now logged in!")
                # return redirect('home')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill the form correctly')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Please update your user info')
            return redirect('update_info')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})


def logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def update_user(request):
    current_user = request.user  # Access the currently logged-in user
    user_form = UpdateUserForm(request.POST or None, instance=current_user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error updating your profile.")

    return render(request, 'update_user.html', {'user_form': user_form})


def update_info(request):
    if request.user.is_authenticated:
        # get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # get current user's shipping info
        # shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get original user for
        form = UserInfoForm(request.POST or None, instance=current_user)
        # get user's shipping form
        # shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        # if request.method == 'POST':
        #     if form.is_valid() or shipping_form.is_valid():
        #         # save original form
        #         form.save()
        #         # save shipping form
        #         shipping_form.save()
        #
        #         messages.success(request, "Your Info has updated successfully!")
        #         return redirect('home')
        #     else:
        #         messages.error(request, "There was an error updating your Info.")

        return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully!")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return render(request, 'update_password.html', {'form': form})

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {})
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('login')



def job_application(request):
    if request.method == 'POST':
        form = InterpreterApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_application_success')  # Replace with your success URL name
    else:
        form = InterpreterApplicationForm()
    return render(request, 'job_application.html', {'form': form})

def job_application_success(request):
    return render(request, 'job_application_success.html')