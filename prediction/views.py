from time import sleep
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import evaluate_dqn
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
def homepage(request):
    result = evaluate_dqn.mainFunction()
    print("2222222222222222222222")

    print("reseult",result)
    print("hellooooooooooooo")
       # return redirect('homepage')
    return render(request, 'index.html')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful!")
#             return redirect("home")  # Redirect to the home page or dashboard
#         else:
#             messages.error(request, "Invalid username or password.")
    
#     return render(request, "login.html")


def callEvaluate(request):
    result = evaluate_dqn.mainFunction()
    return JsonResponse({"prediction": result})