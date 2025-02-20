import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

from my_app.forms import \
    InterpreterApplicationForm, ContactForm, AppointmentForm, ApplicantRegistrationForm, MpesaDonationForm
from my_app.models import Event, EducationalResource, InterpreterApplication, Interpretation, CommunityGroup
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .mpesa_utils import get_mpesa_access_token
from django.http import JsonResponse
from django.http import HttpResponse
from .mpesa_utils import initiate_mpesa_payment
from .sign_recognition import mp_hands, mp_drawing
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import os
import sys
import tensorflow as tf


# Disable TensorFlow during migrations
if "migrate" in sys.argv or "makemigrations" in sys.argv:
    os.environ["DISABLE_TF"] = "1"

# Create your views here.
def home(request):
    events = Event.objects.filter(is_new=True).order_by('-date_created')
    return render(request, 'home.html', {'events': events})


def about(request):
    interpreters = InterpreterApplication.objects.filter(status='approved')
    return render(request, 'about-us.html', {'interpreters': interpreters})


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


def interpreters(request):
    return render(request, 'interpretation.html')


@login_required
def job_application(request):
    if request.method == 'POST':
        form = InterpreterApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Assign logged-in user
            application.save()
            # Send email notification
            # Extract form data
            name = f"{application.first_name} {application.last_name}"
            email = application.email
            phone = application.phone
            experience = application.experience_years
            languages = application.languages
            cover_letter = application.cover_letter

            # Email details
            subject = f"New Interpreter Application from {name}"
            body = (
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Years of Experience: {experience}\n"
                f"Languages: {languages}\n\n"
                f"Cover Letter:\n{cover_letter}"
            )
            recipient_list = ['dinicommunity2024@gmail.com']

            # Create and send email with Reply-To header
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                reply_to=[email]  # Allows replying directly to the applicant
            )

            # Attach resume if provided
            if application.resume:
                email_message.attach(application.resume.name, application.resume.read())

            email_message.send(fail_silently=False)

        return redirect('job_application_success')
    else:
        form = InterpreterApplicationForm()
    return render(request, 'job_application.html', {'form': form})


@login_required
def job_application_success(request):
    return render(request, 'job_application_success.html')


def register_applicant(request):
    if request.method == "POST":
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")  # Redirect to applicant dashboard
    else:
        form = ApplicantRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_applicant(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Redirect to dashboard
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def applicant_dashboard(request):
    applications = InterpreterApplication.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"applications": applications})


@login_required
def edit_interpreter_profile(request):
    try:
        interpreter = InterpreterApplication.objects.get(user=request.user)
    except InterpreterApplication.DoesNotExist:
        interpreter = InterpreterApplication(user=request.user)

    if request.method == 'POST':
        form = InterpreterApplicationForm(request.POST, request.FILES, instance=interpreter)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = InterpreterApplicationForm(instance=interpreter)

    return render(request, 'edit_interpreter_profile.html', {'form': form})


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


def interpretation(request):
    services = Interpretation.objects.all()
    return render(request, 'interpretation.html', {'services': services})


def past_events(request):
    events = Event.objects.filter(is_new=False)  # Get past events
    return render(request, 'past_events.html', {'events': events})


def educational_resources(request):
    resources = EducationalResource.objects.prefetch_related('category').all()
    return render(request, 'educational_resources.html', {'resources': resources})


def community_group(request):
    groups = CommunityGroup.objects.all()
    return render(request, 'community.html', {'groups': groups})


@csrf_exempt  # If you're using ngrok or testing locally, you may need to disable CSRF for testing.
def mpesa_donate(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        # Proceed with the rest of your logic
        # Validate the data and process the M-Pesa payment
        return HttpResponse("Donation successful")
    else:
        return HttpResponse("Invalid method. Please submit via POST.", status=405)


def mpesa_callback(request):
    if request.method == 'POST':
        # Get the response from M-Pesa
        response_data = request.POST
        # Log or process the response as needed (e.g., save payment status to the database)
        print(response_data)
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "failed"}, status=400)




def process_image(request):
    """ Process uploaded images for hand detection """
    if request.method == "POST" and request.FILES.get('image'):
        image = request.FILES['image']
        img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with mp_hands.Hands(static_image_mode=True) as hands:
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imwrite("media/processed_image.jpg", img)
        return JsonResponse({"message": "Image processed successfully!", "image_url": "/media/processed_image.jpg"})

    return JsonResponse({"error": "No image uploaded."})

# Only load the model when needed
model = None
def get_model():
    """Load the model only when needed, but disable it during migrations."""
    global model
    if os.environ.get("DISABLE_TF") == "1":
        return None  # Don't load the model during migrations

    if model is None:
        model = tf.keras.models.load_model("sign_model.h5")
    return model



# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
sentence_queue = deque(maxlen=10)  # Store the last 10 words

def process_live(request):
    model = get_model()
    """ Stream real-time sign recognition """
    def generate_frames():
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                # Convert BGR to RGB for Mediapipe
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Extract hand landmark coordinates
                        landmark_data = np.array(
                            [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                        ).flatten().reshape(1, -1)

                        # Predict sign
                        prediction = model.predict(landmark_data)
                        predicted_label = np.argmax(prediction)

                        # Convert label to text
                        label_map = {0: "hello", 1: "yes", 2: "no", 3: "thank you", 4: "please"}
                        word = label_map.get(predicted_label, "")

                        if word:
                            sentence_queue.append(word)  # Add word to sentence queue

                # Construct translated sentence
                translated_sentence = " ".join(sentence_queue)

                # Encode the frame to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        cap.release()

    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")


def get_translated_text(request):
    """ API endpoint to get the latest translated sentence """
    return JsonResponse({"translated_sentence": " ".join(sentence_queue)})
def sign_video(request):
    return render(request, 'sign_video.html')
