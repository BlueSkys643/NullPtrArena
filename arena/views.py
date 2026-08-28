from django.shortcuts import render

# Create your views here.
def submit(request):
    if request.method == "POST":
        code = request.POST["editor"]
        language = request.POST["language"]
        # run code here

        
    return render(request, "arena/submit.html")