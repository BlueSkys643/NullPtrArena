from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .helper import run_code

# Create your views here.
def submit(request):
    result = "Nothing submitted yet"
    if request.method == "POST":
        code = request.POST["editor"]
        language = request.POST["language"]
        # run code here
        result = run_code(code, language, "reference/test-double.csv")

    return render(request, "arena/submit.html", {"output": result})

def home(request):
    problem_sets = ProblemSet.objects.all()
    problems = Problem.objects.all()
    return render(request, "arena/home.html", {
        "problem_sets": problem_sets,
        "problems": problems,
    })

def login_user(request):
    problem_sets = ProblemSet.objects.all()
    if request.user.is_authenticated:
        submissions = Submission.objects.filter(author=request.user)
    else:
        submissions = Submission.objects.none()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('login')
        else:
            messages.success(request, "There was an error logging in...")
            return redirect('login')
    return render(request, "arena/login.html", {
        "problem_sets": problem_sets,
        "submissions": submissions,
    })

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def sets(request):
    problem_sets = ProblemSet.objects.all()
    return render(request, "arena/sets.html", {
        "problem_sets": problem_sets,
    })


def problem_set(request, id):
    problem_sets = ProblemSet.objects.all()
    problem_set = get_object_or_404(ProblemSet, id=id)
    problems = Problem.objects.filter(problem_set=id)
    return render(request, "arena/problem-set.html", {
        "problem_sets": problem_sets,
        "problem_set": problem_set,
        "problems": problems,
    })