from time import sleep
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import UnusualActivity
from . import evaluate_dqn
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import time
import smtplib  # For sending email
from email.mime.text import MIMEText  # To format email text
from email.mime.multipart import MIMEMultipart  # To create email with subject and body
from . import ev
from .forms import UserRegisterForm

# Create your views here.
def homepage(request):
    result = evaluate_dqn.mainFunction()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print("reseult",result, timestamp) 
       # return redirect('homepage')
    return render(request, 'index2.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("autenticated")
        
        if user is not None:
            login(request, user)
            print("Logged in")
            messages.success(request, "Login successful!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

def callEvaluate(request):
    result = evaluate_dqn.mainFunction()
    pred = ev.main()
    print(pred)
    return JsonResponse({"prediction": result})

def send_mail():

    sender_email = "spinxx360@gmail.com"  
    sender_password = "vmog qjgr ahso tzpz" 
    recipient_emails = ["em.shinojeattath5112@gmail.com"]  # Add recipient emails
    subject = "Test Email from Me"
    body = "Hello,\n\nThis is a test email sent using My code.\n\nBest regards,\nDEF"

    smtp_server = "smtp.gmail.com" 
    smtp_port = 587 

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(sender_email, sender_password)  

        # Step 6: Send email to all recipients
        for recipient in recipient_emails:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send the email
            server.sendmail(sender_email, recipient, msg.as_string())
            print(f"Email sent to {recipient}")


    except Exception as e:
        print(f"Error: {e}")

def news(request):
    return render(request, "news.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        
def report_activity(request):
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        description = request.POST.get('description')
        location = request.POST.get('location')

        UnusualActivity.objects.create(
            user=request.user,
            activity_type=activity_type,
            description=description,
            location=location
        )
        return redirect('home')
    return render(request, 'report_activity.html')