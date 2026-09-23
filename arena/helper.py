
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
