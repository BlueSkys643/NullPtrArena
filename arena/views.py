from django.shortcuts import render

def run_code(code, lang):
    return "runCode function not yet complete."

# Create your views here.
def submit(request):
    result = "Nothing submitted yet"
    if request.method == "POST":
        code = request.POST["editor"]
        language = request.POST["language"]
        # run code here
        result = run_code(code, language)

    return render(request, "arena/submit.html", {"output": result})