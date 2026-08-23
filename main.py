import docker
from datetime import datetime

client = docker.from_env()

output = client.containers.run(
    "python:3.12-slim",
    [
        "python", 
        "-c", 
        """
import time
from datetime import datetime

for _ in range(3):
    print(datetime.now().strftime("%H:%M:%S"), flush=True)
    time.sleep(3)
        """
    ],
    remove=True,
)
print('Container Times')
print(output.decode())
print('System Time')
print(datetime.now().strftime("%H:%M:%S"))
