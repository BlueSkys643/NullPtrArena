from django.shortcuts import render
import docker

def run_code(code, lang):
    if(lang == "python"):
        client = docker.from_env()
        output = client.containers.run(
            "python:3.12-slim",
            [
                "python",
                "-c",
                code,
            ],
            remove=True,

            # Security Settings
            network_mode="none",
            read_only=True,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
            mem_limit="64m",
            nano_cpus=500_000_000,
            pids_limit=64,
        )
        return output.decode()
    else:
        return "language not yet supported"

# Create your views here.
def submit(request):
    result = "Nothing submitted yet"
    if request.method == "POST":
        code = request.POST["editor"]
        language = request.POST["language"]
        # run code here
        result = run_code(code, language)

    return render(request, "arena/submit.html", {"output": result})