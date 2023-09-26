import os

import docker

IMAGE_NAME = "cfrc2694/uniandes-pheno-code-server:latest"
REPO_URL = "https://github.com/Phenomenology-group-uniandes/detectors_school_bootcamp.git"


docker_client = docker.from_env()


async def lauch_container(user_port: int, container_port: int, container_name: str):
    container_options = {
        "image": "cfrc2694/uniandes-pheno-code-server:latest",
        "name": container_name,
        "ports": {f"{container_port}/tcp": user_port},
        "detach": True,
    }

    # create container if not exists
    try:
        container = docker_client.containers.get(container_options["name"])
    except docker.errors.NotFound:
        container = docker_client.containers.create(**container_options)

        # install in code-server in the container
        container.exec_run("curl -fsSL https://code-server.dev/install.sh | sh")

        # configure code-server port
        container.exec_run(f"sed -i 's/8080/{container_port}/g' ~/.config/code-server/config.yaml")

    # start container if not running
    if container.status != "running":
        container.start()

    return container


async def stop_container(container_name: str):
    container = docker_client.containers.get(container_name)
    container.stop()


async def remove_container(container_name: str):
    container = docker_client.containers.get(container_name)
    container.remove()


async def launch_container_from_dockerfile(image_name: str, port: int, environment: dict):
    build_context = os.getcwd()
    dockerfile = os.path.join(build_context, "Dockerfile")

    docker_client.images.build(path=build_context, dockerfile=dockerfile, tag=image_name)

    docker_client.containers.run(
        image=image_name,
        ports={"8080/tcp": port},
        environment=environment,
        detach=True,
    )

    return {"status": "success"}
