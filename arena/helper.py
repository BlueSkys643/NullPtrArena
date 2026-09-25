
import docker
import csv

def run_code(code, lang, test_file):
    pass_text = "PASSED"

    if lang != "python":
        return "language not yet supported"

    client = docker.from_env()

    with open(test_file, newline="") as file:
        tests = list(csv.reader(file))

    for test_input, expected_output in tests:
        container = client.containers.create(
            "python:3.12-slim",
            ["python", "-c", code],
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
        print("testcase")
        print(test_input)

        try:
            sock = container.attach_socket(params={"stdin": 1, "stream": 1})
            container.start()
            stdin_data = "\n".join(test_input.split()) + "\n"
            sock._sock.sendall(stdin_data.encode())
            sock._sock.shutdown(1)

            result = container.wait()

            # Runtime error
            if result["StatusCode"] != 0:
                pass_text = "FAILED"
                print(f"status code: {result["StatusCode"]}")
                # print(container.logs().decode().strip())
                # print(expected_output)
                continue

            output = container.logs().decode().strip()

            # Compare output as text
            if output != expected_output.strip():
                print("--- output mismatch ---")
                # print(output)
                # print(expected_output.strip())
                # print(" ")
                pass_text = "FAILED"

        except Exception:
            pass_text = "FAILED"
            print("60")

        finally:
            container.remove(force=True)

    return pass_text