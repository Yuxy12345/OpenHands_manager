import time
import docker
from random import randint
from dao.container import ContainerDao

try:
    client = docker.from_env()
except docker.errors.DockerException as e:
    raise RuntimeError("Failed to connect to the Docker daemon. Ensure Docker is running and accessible.") from e

container_dao = ContainerDao()

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

def start_container(container_id):
    container = client.containers.get(container_id)
    if container.status != 'running':
        container.start()
        print(f"Container {container_id} started.")
    else:
        print(f"Container {container_id} is already running.")

def stop_inactive_containers(image_name, inactivity_threshold=1800):
    containers = client.containers.list(filters={"ancestor": image_name})
    for container in containers:
        stats = container.stats(stream=False)
        # 获取网络流量统计信息
        networks = stats.get('networks', {})
        total_rx_bytes = sum(interface.get('rx_bytes', 0) for interface in networks.values())

        # 获取容器的上次检查时间
        last_check_time = container.attrs['State']['StartedAt']
        last_check_timestamp = time.mktime(time.strptime(last_check_time, "%Y-%m-%dT%H:%M:%S.%fZ"))

        # 如果网络流量没有变化且超过阈值，停止容器
        if time.time() - last_check_timestamp > inactivity_threshold and total_rx_bytes == 0:
            container.stop()
            container_db = container_dao.get_by_id(container.id)
            container_dao.update_container(container_db, status=False)
            print(f"Stopped inactive container: {container.name}")