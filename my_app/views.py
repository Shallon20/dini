import logging

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

from my_app.forms import \
    InterpreterApplicationForm, ContactForm, AppointmentForm, ApplicantRegistrationForm, MpesaDonationForm, LoginForm
from my_app.models import Event, EducationalResource, InterpreterApplication, Interpretation, CommunityGroup, \
    GalleryImage, FAQ
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import pandas as pd
import threading
import time
from collections import deque, Counter
# from .sign_recognition import predict_sign
# from .sign_recognition import process_frame, predict_sign
# from .data_collection import process_uploaded_file


# Create your views here.
def home(request):
    events = Event.objects.filter(is_new=True).order_by('-date_created')
    images = GalleryImage.objects.all()
    return render(request, 'home.html', {'events': events, 'images': images})


def about(request):
    interpreters = InterpreterApplication.objects.filter(status='approved')
    faqs = FAQ.objects.all()
    return render(request, 'about-us.html', {'interpreters': interpreters, 'faqs': faqs})


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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect("dashboard")
                else:
                    messages.error(request, "Account is inactive.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form is invalid.")

    else:
        form = LoginForm()
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



# Load the trained model
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sign_model.h5"))

if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    model = None  # Prevent crashing if model is missing
    print("ERROR: Model file not found!")

# Load labels dynamically from the dataset
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sign_data.csv"))

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    unique_labels = list(df["label"].unique())  # Keep original order
    label_map = {i: label for i, label in enumerate(unique_labels)}
    print(f"Loaded labels from dataset: {label_map}")  # Debugging output

else:
    label_map = {}  # Empty fallback if CSV is missing
    print("ERROR: sign_data.csv not found!")


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# Store translated text
sentence_queue = deque(maxlen=1)  # Store last 1 word
translated_text = ""  # Stores the last detected sentence
hands_visible = False # Checks if hands are currently detected


def sign_video(request):
    global translated_text
    translated_text = ""  # Resets translation when page loads
    return render(request, 'sign_video.html')

def process_live_translation(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")

# Store past predictions for smoothing
past_predictions = deque(maxlen=5)  # Stores last 5 predictions
# translated_text = ""  # Final translated sentence
# hands_visible = False  # Track hand visibility
lock = threading.Lock()  # Lock for thread-safe updates

def smooth_prediction(predictions, window_size=5):
    """Returns the most common prediction in the last 'window_size' frames,
       but avoids rapid switching between competing words."""
    predictions_list = list(predictions)  # Convert deque to list

    if len(predictions_list) < window_size:
        return predictions_list[-1]  # Use last prediction if window is too small

    counter = Counter(predictions_list[-window_size:])
    most_common = counter.most_common(2)  # Get top 2 predictions

    # If two words appear nearly the same number of times, avoid switching
    if len(most_common) > 1 and abs(most_common[0][1] - most_common[1][1]) < 3:
        return predictions_list[-1]  # Keep the last detected word

    return most_common[0][0]  # Return the most frequent word
def process_frame_for_prediction(landmark_data):
    """Runs TensorFlow prediction in a separate thread to avoid blocking."""
    global translated_text, hands_visible

    if landmark_data.shape[1] == 42:
        prediction = model.predict(landmark_data, verbose=0)
        predicted_label = np.argmax(prediction)

        with lock: # ensures safe access
            # Store past predictions for smoothing
            past_predictions.append(predicted_label)

        # Get the smoothed prediction
        smoothed_label = smooth_prediction(past_predictions)
        word = label_map.get(smoothed_label, "Unknown")

        # Only update if a valid word is detected
        if word != "Unknown":
            with lock:
                sentence_queue.append(word)
                translated_text = " ".join(sentence_queue)
# Function to capture and process video frames
def generate_frames():
    """Capture video frames, process hand landmarks and store words only when hands disappear"""
    global translated_text, hands_visible  # Allow function to update translation globally
    cap = cv2.VideoCapture(0)  # Open webcam

    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return

    frame_counter = 0  # To skip frames for better performance

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Webcam disconnected!")

            break
        frame_counter += 1
        if frame_counter % 2 != 0:  # Process every 2nd frame to reduce CPU load
            continue

        # Convert to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks and model:
            hands_visible = True

            for hand_landmarks in results.multi_hand_landmarks:
                # Extract hand landmark positions (21 x, y coordinates)
                landmark_data = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark]).flatten().reshape(1, -1)

                # Run prediction in a new thread
                threading.Thread(target=process_frame_for_prediction, args=(landmark_data,)).start()


        else:
            # if hands were visible, now they are gone, finalize translation
            if hands_visible:
                print("Hands disappeared! Translating sentence...")
                hands_visible = False # Reset state
                with lock:
                    translated_text = ""  # Clear translation when hands disappear
                    sentence_queue.clear()  # Clear previous words

        # Convert frame back to JPEG format
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# API to send the translated text to the frontend
def get_translated_text(request):
    global translated_text
    if translated_text == "":  # ✅ If no hands, send empty translation
        return JsonResponse({"translated_sentence": "Waiting for translation..."})
    print(f" Sending translated text to frontend: {translated_text}")  # Debugging output
    return JsonResponse({"translated_sentence": translated_text})

def upload(request):
    return render(request, 'upload.html')

