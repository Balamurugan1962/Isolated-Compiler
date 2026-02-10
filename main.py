import docker


def main():
    client = docker.from_env()

    try:
        image = client.images.pull("python:3-slim")
        val = client.containers.run(image, ["python", "-c", "print('Hello')"])
        print(val.decode())

    except Exception as e:
        print(f"An error occurred: \n\t{e}")


if __name__ == "__main__":
    main()
