import docker
from random import randint

client = docker.from_env()

def create_user_container(user_id):
    # 随机生成外部端口（示例范围 8000-9000）
    port = randint(8000, 9000)

    # 创建容器
    container = client.containers.run(
        name=f"OpenHands-{str(user_id)}"
        "docker.all-hands.dev/all-hands-ai/openhands:latest",
        detach=True,
        ports={'3000/tcp': port},
        labels={"user_id": str(user_id)},
        extra_hosts={'host.docker.internal': 'host-gateway'}
    )
    return {
        "container_id": container.id,
        "port": port
    }

def find_user_container(user_id):
    containers = client.containers.list(
        filters={"label": f"user_id={user_id}"}
    )
    return containers[0] if containers else None