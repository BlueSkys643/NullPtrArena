from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import docker
import csv

def run_code(code, lang, test_file):
    passText = "Passed"
    if(lang == "python"):
        client = docker.from_env()

        with open(test_file, newline="") as file:
            tests = list(csv.reader(file))

        for test_input, expected_output in tests:
            #print("test in:  ", test_input)
            #print("expected: ", expected_output)
        
            container = client.containers.create(
                "python:3.12-slim",
                [
                    "python",
                    "-c",
                    code,
                ],
                stdin_open=True,

                # Security Settings
                network_mode="none",
                read_only=True,
                cap_drop=["ALL"],
                security_opt=["no-new-privileges"],
                mem_limit="64m",
                nano_cpus=500_000_000,
                pids_limit=64,
            )

            try:
                container.start()
                sock = container.attach_socket(params={"stdin": 1, "stream": 1})
                sock._sock.sendall((test_input + '\n').encode())
                sock._sock.shutdown(1)  # Send EOF

                result = container.wait()

                output = container.logs().decode()

                #print("Output:", output)

                if (int(output.strip()) != int(expected_output.strip())):
                    #print("AAA: ", test_input)
                    passText = "Failed"

            finally:
                container.remove(force=True)


        return passText
    else:
        return "language not yet supported"

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

def problem_set(request, id):
    problem_sets = ProblemSet.objects.all()
    problem_set = get_object_or_404(ProblemSet, id=id)
    problems = Problem.objects.filter(problem_set=id)
    return render(request, "arena/problem-set.html", {
        "problem_sets": problem_sets,
        "problem_set": problem_set,
        "problems": problems,
    })