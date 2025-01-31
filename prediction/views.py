from time import sleep
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import evaluate_dqn
# Create your views here.
def homepage(request):

    result = evaluate_dqn.mainFunction()
    print("2222222222222222222222")

    print("reseult",result)
    print("hellooooooooooooo")
       # return redirect('homepage')
    return render(request, 'index.html', {"result":result})

def callEvaluate(request):
    result = evaluate_dqn.mainFunction()
    return JsonResponse({"prediction": result})