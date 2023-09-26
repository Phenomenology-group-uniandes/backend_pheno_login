import os

import docker
from fastapi import APIRouter

# from .task import launch_container_from_dockerfile

container_router = APIRouter(
    prefix="/container",
    tags=["container"],
)


@container_router.get("/list")
async def list_containers():
    docker_client = docker.from_env()
    containers = docker_client.containers.list()

    return {"containers": list(containers)}


@container_router.post("/create_container_from_dockerfile")
async def create_container_from_dockerfile(container_name: str, port: int, password: str):
    client = docker.from_env()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    dockerfile_path = os.path.join(current_directory, "code-server.Dockerfile")
    client.images.build(path=".", dockerfile=dockerfile_path, tag=container_name)
    client.containers.run(
        image=container_name,
        ports={"8080/tcp": port},
        environment={"PASSWORD": password},
        detach=True,
        network="repos_uniandes_pheno_network",
    )

    return {"container_name": container_name, "port": port, "password": password, "status": "created"}
