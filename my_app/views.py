from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from my_app.forms import LoginForm, SignupForm, UpdateUserForm, UserInfoForm, ChangePasswordForm, \
    InterpreterApplicationForm, ContactForm, AppointmentForm
from my_app.models import Profile, Event
from django.conf import settings


# Create your views here.
def home(request):
    events = Event.objects.filter(is_new=True).order_by('-date_created')
    return render(request, 'home.html', {'events': events})


def about(request):
    return render(request, 'about-us.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Email details
            subject = f"Contact Us message from {name}"
            body = f"Message from: {name}\nEmail: {email}\n\n{message}"
            recipient_list = ['dinicommunity2024@gmail.com']

            # Create and send email with Reply-To header
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                reply_to=[email]
            )
            email_message.send(fail_silently=False)

            # Render confirmation message
            return render(request, 'contact-us.html', {'name': name})

    else:
        form = ContactForm()

    return render(request, 'contact-us.html', {'form': form})
def gallery(request):
    return render(request, 'gallery.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def interpreters(request):
    return render(request, 'online_interpretation.html')


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


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            service_type = form.cleaned_data['service_type']
            message = form.cleaned_data['message']
            date = form.cleaned_data['date']

            # Email details
            subject = f"Appointment Booking from {name}"
            body = (
                f"Message from: {name}\n"
                f"Phone Number: {phone}\n"
                f"Email: {email}\n"
                f"Appointment Date: {date}\n"
                f"Service Type: {service_type}\n\n"
                f"Full Message: {message}"
            )
            recipient_list = ['dinicommunity2024@gmail.com']

            # Send email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                reply_to=[email]
            )
            email_message.send(fail_silently=False)

            # Success message
            return render(request, 'appointment.html', {
                'form': AppointmentForm(),  # Reset form
                'success': 'Your appointment request has been submitted successfully!'
            })

    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', {'form': form})
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


def online_interpretation(request):
    return render(request, 'online_interpretation.html')


def virtual_interpretation(request):
    return render(request, 'virtual_interpretation.html')


def past_events(request):
    events = Event.objects.filter(is_new=False)  # Get past events
    return render(request, 'past_events.html', {'events': events})