import io
import tarfile

import docker


def tarStream(code, fileEx):
    tarstream = io.BytesIO()
    with tarfile.open(fileobj=tarstream, mode="w") as tar:
        data = code.encode()
        info = tarfile.TarInfo(name=f"main.{fileEx}")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))

    tarstream.seek(0)
    return tarstream


def main():
    client = docker.from_env()
    code = 'print("Hello")\n'

    image = "python:3-slim"
    client.images.pull(image)

    container = client.containers.create(
        image=image, command="sleep infinity", tty=True
    )

    try:
        container.start()
        tarstream = tarStream(code, "py")
        container.put_archive("/", tarstream)

        exec_result = container.exec_run(["python", "/main.py"])

        print(exec_result.output.decode().strip())

    finally:
        container.remove(force=True)


if __name__ == "__main__":
    main()
