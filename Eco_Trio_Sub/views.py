from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
from .models import Registration,TeamMember,Collaboration
from django.utils.dateparse import parse_datetime
from django.contrib import messages
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import Job

EMAIL_HOST_USER = 'annaluruchaitanya@gmail.com'


# (Keep this if you want to reuse OTP later)
@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email or '@' not in email:
            return JsonResponse({'message': 'Invalid email address'}, status=400)

        otp = str(random.randint(1000, 9999))

        try:
            send_mail(
                subject='Your OTP from Eco Trio Solutions',
                message=f'Your OTP is: {otp}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            request.session['otp'] = otp
            request.session['email'] = email
            print("OTP Sent:", otp)
            return JsonResponse({'message': 'OTP sent successfully'})
        except Exception as e:
            print("Email Error:", e)
            return JsonResponse({'message': f'Failed to send OTP: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        # Process your form data here
        first_name = request.POST.get('first_name')
        # ... handle the rest

        return HttpResponse("Form submitted successfully!")
    return HttpResponse("Only POST allowed")


# ✅ UPDATED SIGNUP VIEW WITHOUT OTP
from django.contrib.auth import authenticate, login

def signup_view(request):
    if request.method == "GET":
        if not request.session.get('registered'):
            return redirect('/register/')
        return render(request, 'signup.html')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation checks
        if not all([name, email, phone, location, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists.")
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        user.save()

        # ✅ Auto login after signup
        authenticated_user = authenticate(username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, f"Welcome {name}! Your account has been created.")

        return redirect('home')

    return render(request, 'signup.html')



# def signup_view(request):
#     if request.method == "GET":
#         if not request.session.get('registered'):
#             return redirect('/register/')
#         return render(request, 'signup.html')
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         location = request.POST.get('location')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if not all([name, email, phone, location, password, confirm_password]):
#             messages.error(request, "All fields are required.")
#             return render(request, 'signup.html')

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'signup.html')

#         if User.objects.filter(username=email).exists():
#             messages.error(request, "User with this email already exists.")
#             return render(request, 'signup.html')

#         user = User.objects.create_user(
#             username=email,
#             email=email,
#             password=password,
#             first_name=name
#         )
#         user.save()

#         # ✅ You can save phone/location to a Profile model if needed.

#         messages.success(request, "Signup successful. Please login.")
#         return redirect('home')

#     return render(request, 'signup.html')


# def signin_view(request):
#     if request.method == "GET":
#         if not request.session.get('registered'):
#             return redirect('/register/')
#         return render(request, 'signin.html')
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(username=email, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome {user.first_name}!")
#             return redirect('/home')
#         else:
#             messages.error(request, "Invalid email or password.")
#             return render(request, 'signin.html')

#     return render(request, 'signin.html')



def signin_view(request):
    if request.method == "GET":
        # if not request.session.get('registered'):
        #     return redirect('/register/')
        return render(request, 'signin.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # First, check if the email exists in DB
        try:
            user_obj = User.objects.get(username=email)  # or filter by email field if using a custom user model
        except User.DoesNotExist:
            messages.error(request, "Email is not registered.")
            return render(request, 'signin.html')

        # If email exists, check password
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}!")
            return redirect('/home')
        else:
            messages.error(request, "Incorrect password.")
            return render(request, 'signin.html')

    return render(request, 'signin.html')


def logout_view(request):
    logout(request)
    return redirect('signin')

# def register_view(request):
#     if request.method == 'POST':
#         data = request.POST
#         if data.get('first_name') and data.get('phone') and data.get('occupation') and data.get('interest'):
#             # Save to database
#             Registration.objects.create(
#                 first_name=data.get('first_name'),
#                 last_name=data.get('last_name'),
#                 phone=data.get('phone'),
#                 email=data.get('email'),
#                 occupation=data.get('occupation'),
#                 interest=data.get('interest'),
#                 signup_time=datetime.datetime.now(),
#                 device_info=data.get('device_info'),
#             )

#             # Send mail to admin
#             subject = f"New Registration Submission from {data.get('first_name')}"
#             body = f"""
# 📬 New Inquiry/Registration:

# 👤 Name: {data.get('first_name')} {data.get('last_name')}
# 📞 Phone: {data.get('phone')}
# 📧 Email: {data.get('email')}
# 💼 Occupation: {data.get('occupation')}
# 🧠 Interest: {data.get('interest')}
# 🖥️ Device Info: {data.get('device_info')}
# ⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# """
#             send_mail(
#                 subject,
#                 body,
#                 settings.EMAIL_HOST_USER,
#                 ['ecotriosolutionweb@gmail.com'],
#                 fail_silently=False,
#             )

#             request.session['registered'] = True
#             return redirect('/home')
#         else:
#             return render(request, 'register.html', {'error': 'Please fill all required fields.'})
#     return render(request, 'register.html')

import requests

# def register_view(request):
#     if request.user.is_authenticated:
#         if Registration.objects.filter(email=request.user.email).exists():
#             return redirect('/home')
        
#     if request.method == 'POST':
#         data = request.POST
#         if data.get('first_name') and data.get('phone') and data.get('occupation') and data.get('interest'):
#             Registration.objects.create(
#                 first_name=data.get('first_name'),
#                 last_name=data.get('last_name'),
#                 phone=data.get('phone'),
#                 email=data.get('email'),
#                 occupation=data.get('occupation'),
#                 interest=data.get('interest'),
#                 signup_time=timezone.now(),
#                 device_info=data.get('device_info'),
#             )

#             # 📧 Email to admin
#             subject = f"New Registration Submission from {data.get('first_name')}"
#             body = f"""
# 📬 New Inquiry/Registration:

# 👤 Name: {data.get('first_name')} {data.get('last_name')}
# 📞 Phone: {data.get('phone')}
# 📧 Email: {data.get('email')}
# 💼 Occupation: {data.get('occupation')}
# 🧠 Interest: {data.get('interest')}
# 🖥️ Device Info: {data.get('device_info')}
# ⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# """
#             send_mail(
#                 subject,
#                 body,
#                 settings.EMAIL_HOST_USER,
#                 ['ecotriosolutionweb@gmail.com'],
#                 fail_silently=False,
#             )

#             request.session['registered'] = True
#             return redirect('/home')
#         else:
#             return render(request, 'register.html', {'error': 'Please fill all required fields.'})
#     return render(request, 'register.html')


def home_view(request):
    # if not request.session.get('registered'):
    #     return redirect('/register/')
    return render(request, 'index.html')


def agri_services_view(request):
    return render(request, "agri_service.html")


def global_view(request):
    # if not request.session.get('registered'):
    #     return redirect('/register/')
    return render(request, 'go_global.html')

def digital_grow(request):
    # if not request.session.get('registered'):
    #     return redirect('/register/')
    return render(request, 'digital.html')

def team_view(request):
    # if not request.session.get('registered'):
    #     return redirect('/register/')
    #return render(request, 'team.html')
    team_members = TeamMember.objects.all()
    return render(request, 'team.html', {'team_members': team_members})


from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Registration
def register_view(request):
    """
    Handles registration form submissions for customer inquiries.
    Saves inquiry to DB, sends notification email to admin,
    and posts data to Google Form.
    """
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        occupation = request.POST.get('occupation')
        interest = request.POST.get('interest')
        looking_for = request.POST.get('looking_for')

        # Validate all fields
        if not all([username, email, phone, occupation, interest, looking_for]):
            messages.error(request, 'Please fill all required fields.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            # Save to DB
            Registration.objects.create(
                username=username,
                email=email,
                phone=phone,
                occupation=occupation,
                interest=interest,
                looking_for=looking_for,
                signup_time=timezone.now(),
            )

            # Post to Google Form (optional)
            google_form_url = "https://docs.google.com/forms/d/e/YOUR_GOOGLE_FORM_ID/formResponse"
            google_form_data = {
                "entry.1111111111": username,
                "entry.2222222222": email,
                "entry.3333333333": phone,
                "entry.4444444444": occupation,
                "entry.5555555555": interest,
                "entry.6666666666": looking_for,
            }
            try:
                requests.post(google_form_url, data=google_form_data)
            except Exception as e:
                print(f"Google Form submission failed: {e}")

            # Send email directly to ecotriosolutionweb@gmail.com
            subject = f"New Inquiry: {username}"
            body = f"""
A new user has submitted an inquiry:

Name: {username}
Email: {email}
Phone: {phone}
Occupation: {occupation}
Area of Interest: {interest}
Looking For: {looking_for}
Submission Time: {timezone.now()}
"""
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,   # sender's Gmail
                ['ecotriosolutionweb@gmail.com'],  # direct recipient
                fail_silently=False,
            )

            messages.success(request, 'Thank you for your interest! We have received your details and will contact you shortly.')
            request.session['has_registered'] = True
            return redirect(request.META.get('HTTP_REFERER', '/'))

        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, 'An error occurred during submission. Please try again.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'index.html')



#Main registerview function
# def register_view(request):
#     # ✅ Step 1: If already registered in session, skip
#     if request.session.get('registered'):
#         return redirect('/home')

#     # ✅ Step 2: If logged in, check DB by email
#     if request.user.is_authenticated:
#         if Registration.objects.filter(email=request.user.email).exists():
#             request.session['registered'] = True
#             return redirect('/home')

#     # ✅ Step 3: POST - Handle new registration
#     if request.method == 'POST':
#         data = request.POST
#         email = data.get('email')

#         # Check if already in DB
#         if Registration.objects.filter(email=email).exists():
#             request.session['registered'] = True
#             return redirect('/home')

#         if data.get('first_name') and data.get('phone') and data.get('occupation') and data.get('interest'):
#             # Save to DB
#             Registration.objects.create(
#                 first_name=data.get('first_name'),
#                 last_name=data.get('last_name'),
#                 phone=data.get('phone'),
#                 email=email,
#                 occupation=data.get('occupation'),
#                 interest=data.get('interest'),
#                 signup_time=timezone.now(),
#                 device_info=data.get('device_info'),
#             )

#             # 📧 Email to admin
#             subject = f"New Registration Submission from {data.get('first_name')}"
#             body = f"""
# 📬 New Inquiry/Registration:

# 👤 Name: {data.get('first_name')} {data.get('last_name')}
# 📞 Phone: {data.get('phone')}
# 📧 Email: {email}
# 💼 Occupation: {data.get('occupation')}
# 🧠 Interest: {data.get('interest')}
# 🖥️ Device Info: {data.get('device_info')}
# ⏰ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# """
#             send_mail(
#                 subject,
#                 body,
#                 settings.EMAIL_HOST_USER,
#                 ['ecotriosolutionweb@gmail.com'],
#                 fail_silently=False,
#             )

#             # Mark as registered in session
#             request.session['registered'] = True

#             return redirect('/home')
#         else:
#             return render(request, 'register.html', {'error': 'Please fill all required fields.'})

#     # ✅ Step 4: Show form only if not registered
#     return render(request, 'register.html')



def contact_view(request):
    if request.method == "GET":
        # if not request.session.get('registered'):
        #     return redirect('/register/')
        return render(request, 'contact.html')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        address = request.POST.get('address', '')
        message = request.POST.get('message', '')

        if name and email and mobile and address and message:
            subject = f"New Contact Message from {name}"
            body = f"""
New Contact Submission:

Name: {name}
Email: {email}
Mobile: {mobile}
Address: {address}

Message:
{message}
"""

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                ['ecotriosolutionweb@gmail.com'],  # Change to your receiving email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill out all fields.')

    return render(request, 'contact.html')


def collab_view(request):
    # if not request.session.get('registered'):
    #     return redirect('/register/')
    collaborations = Collaboration.objects.all()
    jobs = Job.objects.all()
    return render(request, 'collab.html', {'collaborations': collaborations,'jobs':jobs})


def apply_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        apartment = request.POST.get('apartment')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        consent = request.POST.get('consent')
        cv = request.FILES.get('cv')  # FileField (optional)

        # ✅ Email to Admin with CV attached
        subject = f"New Job Application: {name} for {job.title}"
        message = (
            f"Job Title: {job.title}\n"
            f"Location: {job.location}\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Street: {street}\n"
            f"Apartment: {apartment}\n"
            f"City: {city}\n"
            f"State: {state}\n"
            f"ZIP: {zip_code}\n"
            f"CV: {cv}\n"
            f"Consent Given: {'Yes' if consent else 'No'}"
        )

        email_msg = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['ecotriosolutionweb@gmail.com'],
        )

        if cv:
            email_msg.attach(cv.name, cv.read(), cv.content_type)
        email_msg.send(fail_silently=False)

        # ✅ Auto-reply to applicant
        applicant_subject = f"Thank you for applying - {job.title} at Eco Trio"
        applicant_message = (
             
            f"Hi {name},\n\n"
            f"Thank you for applying for the role of '{job.title}' at Eco Trio Solutions.\n"
            f"Our team has received your application and we will review it shortly.\n\n"
            f"Role: {job.title}\n"
            f"Location: {job.location}\n\n"
            f"If shortlisted, we will get in touch with you via email or phone.\n\n"
            f"Best regards,\n"
            f"Eco Trio Team"
         )


        send_mail(
            applicant_subject,
            applicant_message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Application submitted successfully!")
        return redirect(request.path) # Replace with your thank-you page
    return render(request, 'apply_job.html', {'job': job})

def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            # ✅ Email to admin
            admin_subject = "New Newsletter Subscription"
            admin_message = f"📩 New subscriber: {email}"
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['ecotriosolutionweb@gmail.com'],  # your admin email
                fail_silently=False,
            )

            # ✅ Email to user
            user_subject = "Thanks for subscribing to Eco Trio!"
            user_message = (
                f"Hi, \n\n"
                f"Thank you for subscribing to Eco Trio Solutions updates.\n"
                f"You'll now receive updates, news, and job opportunities from us.\n\n"
                f"Best regards,\nEco Trio Team"
            )
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")

        return redirect(request.path)  # return to same page

    return redirect('/home')