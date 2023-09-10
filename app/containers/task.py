import docker

docker_client = docker.from_env()


async def lauch_container(
    user_port: int, container_port: int, container_name: str
):
    container_options = {
        "image": "jjonesperez/pucp-madgraph-pythia-delphes:0.7",
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
        container.exec_run(
            "curl -fsSL https://code-server.dev/install.sh | sh"
        )

        # configure code-server port
        container.exec_run(
            f"sed -i 's/8080/{container_port}/g' ~/.config/code-server/config.yaml"
        )

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
