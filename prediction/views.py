from time import sleep
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import evaluate_dqn
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import time
import smtplib  # For sending email
from email.mime.text import MIMEText  # To format email text
from email.mime.multipart import MIMEMultipart  # To create email with subject and body
from . import ev2

# Create your views here.
def homepage(request):
    result = evaluate_dqn.mainFunction()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print("reseult",result, timestamp) 
       # return redirect('homepage')
    return render(request, 'index.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")


def callEvaluate(request):
    result = evaluate_dqn.mainFunction()
    pred = ev2.main()
    print(result)
    return JsonResponse({"prediction": result})

# def send_mail():

#     sender_email = "spinxx360@gmail.com"  
#     sender_password = "vmog qjgr ahso tzpz" 
#     recipient_emails = ["em.shinojeattath5112@gmail.com"]  # Add recipient emails
#     subject = "Test Email from Me"
#     body = "Hello,\n\nThis is a test email sent using My code.\n\nBest regards,\nDEF"

#     smtp_server = "smtp.gmail.com" 
#     smtp_port = 587 

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls() 
#         server.login(sender_email, sender_password)  

#         # Step 6: Send email to all recipients
#         for recipient in recipient_emails:
#             # Create the email message
#             msg = MIMEMultipart()
#             msg["From"] = sender_email
#             msg["To"] = recipient
#             msg["Subject"] = subject
#             msg.attach(MIMEText(body, "plain"))

#             # Send the email
#             server.sendmail(sender_email, recipient, msg.as_string())
#             print(f"Email sent to {recipient}")


#     except Exception as e:
#         print(f"Error: {e}")